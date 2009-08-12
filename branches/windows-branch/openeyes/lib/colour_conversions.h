#define YUV2RGB(y, u, v, r, g, b)\
  r = y + ((v*1436) >> 10);\
  g = y - ((u*352 + v*731) >> 10);\
  b = y + ((u*1814) >> 10);\
  r = r < 0 ? 0 : r;\
  g = g < 0 ? 0 : g;\
  b = b < 0 ? 0 : b;\
  r = r > 255 ? 255 : r;\
  g = g > 255 ? 255 : g;\
  b = b > 255 ? 255 : b

//----------------------- uyyvyy (i.e. YUV411) to rgb24 -----------------------//
void uyyvyy2rgb (unsigned char *src, unsigned char *dest, unsigned long long int NumPixels)
{
  register int i = NumPixels + ( NumPixels >> 1 )-1;
  register int j = NumPixels + ( NumPixels << 1 )-1;
  register int y0, y1, y2, y3, u, v;
  register int r, g, b;

  while (i > 0) {
    y3 = (unsigned char) src[i--];
    y2 = (unsigned char) src[i--];
    v  = (unsigned char) src[i--] - 128;
    y1 = (unsigned char) src[i--];
    y0 = (unsigned char) src[i--];
    u  = (unsigned char) src[i--] - 128;
    YUV2RGB (y3, u, v, r, g, b);
    dest[j--] = r;
    dest[j--] = g;
    dest[j--] = b;
    YUV2RGB (y2, u, v, r, g, b);
    dest[j--] = r;
    dest[j--] = g;
    dest[j--] = b;
    YUV2RGB (y1, u, v, r, g, b);
    dest[j--] = r;
    dest[j--] = g;
    dest[j--] = b;
    YUV2RGB (y0, u, v, r, g, b);
    dest[j--] = r;
    dest[j--] = g;
    dest[j--] = b;
  }
}
