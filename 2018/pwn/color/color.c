#include <arpa/inet.h>
#include <errno.h>
#include <grp.h>
#include <pwd.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define IMAGE_MAX_SIZE (1000000 * 3)
#define UPPER_BOUND    (3000030)

uint8_t hsv_buf[IMAGE_MAX_SIZE];

#pragma pack(push, 1)
struct rcvd
{
    int num_pixels;
    int bytes_recvd;
    int curr_recv;
    int bytes_sent;
    int curr_sent;
    uint8_t rgb_buf[IMAGE_MAX_SIZE];
};
#pragma pack(pop)

void convert_image(uint8_t* rgb_buf, uint32_t pixel_len)
{
    for (uint32_t i = 0; i < pixel_len; i++)
    {
        double r = rgb_buf[i * 3] / 255.0;
        double g = rgb_buf[i * 3 + 1] / 255.0;
        double b = rgb_buf[i * 3 + 2] / 255.0;
        double cmax, cmin;
        if (r >= g && r >= b) {
            cmax = r;
        } else if (g >= r && g >= b) {
            cmax = g;
        } else {
            cmax = b;
        }
        if (r <= g && r <= b) {
            cmin = r;
        } else if (g <= r && g <= b) {
            cmin = g;
        } else {
            cmin = b;
        }
        double delta = cmax - cmin;
        uint32_t h;
        if (delta == 0) {
            h = 0;
        } else if (cmax == r) {
            double tmp = (g - b) / delta;
            if (tmp < 0) {
                tmp *= -1;
            }
            while (tmp > 6) {
                tmp -= 6;
            }
            h = (uint32_t)(60 * tmp);
        } else if (cmax == g) {
            h = (uint32_t)(60 * (((b - r) / delta) + 2));
        } else {
            h = (uint32_t)(60 * (((r - g) / delta) + 4));
        }

        double s_f;
        if (cmax == 0) {
            s_f = 0;
        } else {
            s_f = delta / cmax;
        }

        h = (uint8_t)(h * 255.0 / 360.0);
        uint8_t s = (uint8_t)(s_f * 255);
        uint8_t v = (uint8_t)(cmax * 255);

        hsv_buf[i * 3] = h;
        hsv_buf[i * 3 + 1] = s;
        hsv_buf[i * 3 + 2] = v;
    }
}

int handle_request(int socket_fd)
{
    struct rcvd rcvd;

    if (recv(socket_fd, &rcvd.num_pixels, sizeof(rcvd.num_pixels), 0) != 4) {
        return -1;
    }

    rcvd.num_pixels = htonl(rcvd.num_pixels);

    rcvd.bytes_recvd = 0;
    while (rcvd.bytes_recvd < (3 * rcvd.num_pixels)) {
        rcvd.curr_recv = recv(socket_fd, rcvd.rgb_buf + rcvd.bytes_recvd,
                              (3 * rcvd.num_pixels) - rcvd.bytes_recvd, 0);
        if (rcvd.curr_recv < 0) {
             _exit(-1);
        }
        rcvd.bytes_recvd += rcvd.curr_recv;
        if (rcvd.bytes_recvd > UPPER_BOUND) {
             _exit(-1);
        }
    }

    convert_image(rcvd.rgb_buf, rcvd.num_pixels);

    rcvd.bytes_sent = 0;
    while (rcvd.bytes_sent < (3 * rcvd.num_pixels)) {
        rcvd.curr_sent = send(socket_fd, (char*)(hsv_buf) + rcvd.bytes_sent,
                              (3 * rcvd.num_pixels) - rcvd.bytes_sent, 0);
        if (rcvd.curr_sent < 0) {
            return -1;
        }
        rcvd.bytes_sent += rcvd.curr_sent;
    }
    return 0;
}

int drop_privs(char* username)
{
    struct passwd* pw = getpwnam(username);
    if (pw == NULL)
    {
        printf("Username not found\n");
        return 1;
    }
    if (chdir(pw->pw_dir) != 0)
    {
        printf("Failed to change directory\n");
        return 1;
    }
    if (setgroups(0, NULL) != 0)
    {
        printf("Failed to strip supplemental groups\n");
        return 1;
    }
    if (setgid(pw->pw_gid) != 0)
    {
        printf("Failed to change groupid\n");
        return 1;
    }
    if (setuid(pw->pw_uid) != 0)
    {
        printf("Failed to change uid\n");
        return 1;
    }
    return 0;
}

int main()
{
    if (signal(SIGCHLD, SIG_IGN) == SIG_ERR)
    {
        printf("Failed to set SIGCHLD handler\n");
        return 1;
    }
    struct sockaddr_in saddr;
    memset(&saddr, 0, sizeof(struct sockaddr_in));
    int socket_fd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (socket_fd == -1)
    {
        printf("Failed to create socket\n");
        return 1;
    }

    saddr.sin_family = AF_INET;
    saddr.sin_addr.s_addr = htonl(INADDR_ANY);
    saddr.sin_port = htons(37123);

    if (bind(socket_fd, (struct sockaddr*)(&saddr), sizeof(saddr)) != 0)
    {
        printf("Failed to bind socket\n");
        return 1;
    }
    if (listen(socket_fd, 25) != 0)
    {
        printf("Failed to start listening\n");
        return 1;
    }

    while (1)
    {
        int client_fd = accept(socket_fd, NULL, NULL);
        if (client_fd == -1)
        {
            printf("Error accepting client.  Continuing...\n");
            continue;
        }

        pid_t pid = fork();
        if (pid == -1)
        {
            printf("Error forking.  Continuing...\n");
            continue;
        }
        if (pid == 0)
        {
            alarm(60*10);
            close(socket_fd);
            if (drop_privs("h3") == 0)
            {
                handle_request(client_fd);
                close(client_fd);
                printf("Returned correctly\n");
                _exit(0);
            }
            close(client_fd);
            _exit(0);
        }
        close(client_fd);
    }
}
