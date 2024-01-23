codigo1 = "j2/(o+28s8X/i8D)m\\97a9_@r0O9+39g6Q}o0&-n{02ç6T&a2S3l=66vgJ)e3G1s?95s#@d9,wa<11/I}s9Ahi+00lu{\"v8?2a:\"1!iE=[7]o~`L4(1+[<9VtB({4/j\"&,0c9=\\(2\\e?<+0|p)@<6yts#-9za&>_9$y#%t0aou:k2xb]:.2jr2-j4;a4\"q1&s4!h4]s6~r2}k0,j2\"b3|a9*x9-i2<k0^y9#f3+p3!u5[x0:s8'f9$n0^e7'z7)o9]c3<d1{f8'b5~z1$r1_m4.g3#w2+w7`p8;i6$r8]x1,v5\"y3+n9+e1#j6_s8_n9\"i2\"x0\"c7;m0#a1_c2=j0:k9,f2,c7(n8>d1\"n8,n8^v2/r9\"y6^f0:b5+i3:h3&n3+y7[a9(c2~k9&t8)d2+z5&w0:l1@a8?y7-q7}p4\"e7$s8@q3/s4|n1:f6@m7+h5*a7`o9{r2!r0?v5{b1$o0`w3.o0!a7~p9$w4%x2[u5&y4>r9.u6'l4,i2|m4!t4+s6^d4`i5#m5'k7\\n3'g7:o9-o3>s6'm9}d1<o3(w4<w7}r8.y7,d1}y8'o9;a6<x6'x3~b9|y6!e3@v7\"b2-"
codigo2 = "j2/(o+28s8X/i8D)m\\97a9_@r0O9+39g6Q}o0&-n{02ç6T&a2S3l=66vgJ)e3G1s?95s#@d9,wa<11/I}s9Ahi+00lu{\"v8?2a:\"1!iE=[7]o~`L4(1+[<9VtB({4/j\"&,0c9=\\(2\\e?<+0|p)@<6yts#-9za&>_9$y#%t0aou:k2xb]:.2jr2-j4;a4\"q1&s4!h4]s6~r2}k0,j2\"b3|a9*x9-i2<k0^y9#f3+p3!u5[x0:s8'f9$n0^e7'z7)o9]c3<d1{f8'b5~z1$r1_m4.g3#w2+w7`p8;i6$r8]x1,v5\"y3+n9+e1#j6_s8_n9\"i2\"x0\"c7;m0#a1_c2=j0:k9,f2,c7(n8>d1\"n8,n8^v2/r9\"y6^f0:b5+i3:h3&n3+y7[a9(c2~k9&t8)d2+z5&w0:l1@a8?y7-q7}p4\"e7$s8@q3/s4|n1:f6@m7+h5*a7`o9{r2!r0?v5{b1$o0`w3.o0!a7~p9$w4%x2[u5&y4>r9.u6'l4,i2|m4!t4+s6^d4`i5#m5'k7\\n3'g7:o9-o3>s6'm9}d1<o3(w4<w7}r8.y7,d1}y8'o9;a6<x6'x3~b9|y6!e3@v7\"b2-"


# Verificando se cada caractere é igual
for char1, char2 in zip(codigo1, codigo2):
    if char1 != char2:
        print(f"Os caracteres não são iguais: {char1} != {char2}")
        break
else:
    print("Todos os caracteres são iguais.")
