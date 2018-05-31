import gmpy
import fractions
from scipy.optimize import fsolve

n = 370099671033141588376175581756360980424491995580600109524304692636792296120563363822977313410192016444986004859764911043147546964441891697775267469000813669187672202081765367588450379462043354336198833248696996620972969
e = 65537
p = 10513733234846849736873637829838635104309714688896631127438692162131857778044158273164093838937083421380041997
q = 35201546659608842026088328007565866231962578784643756647773109869245232364730066609837018108561065242031153677
bits = 181
phi = (p-1) * (q-1)
frac = 2**bits
d = gmpy.invert(e, phi)

recovered =  bin(d)[-3:][::-1]
recovered = (int(recovered, 2))

left_reduced = (e * recovered) % frac - 1

for k in range(1,e):
	out = ((n + 1) * k - left_reduced) % frac
	if out == 0:
		to_return = 0
	else:
		if fractions.gcd(k, frac) == 1:
			counter = 1
			calc = (n+1) * k - left_reduced
			current = k * counter
			while current % frac != calc % frac:
				counter += 1
				current = k * counter
			to_return = counter
		else:
			to_return = -1

	if to_return != -1:
		print k
		checked = (-1 * n) % frac
		for i in range(frac):
			if (i*(i - to_return)) % frac == checked and (i-to_return) >=0:
				p0 = i
				q0 = gmpy.invert(i, frac)
				r = 2 **bits
				print(p0, int(q0))
				break
