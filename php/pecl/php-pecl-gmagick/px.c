#include <stdio.h>
#include <wand/wand_api.h>

int main(int argc, char *argv[])
{
	PixelWand *pix;
	char *str;
	char *col[] = {"rgb(0,0,0)", "rgb(80,80,80)", "rgb(255,255,255)", "rgb(999,999,999)", NULL};
	int  i;

	pix = NewPixelWand();
	for (i=0 ; col[i] ; i++) 
	{
		PixelSetColor(pix, col[i]);
		str = PixelGetColorAsString(pix);
		printf("%s = rgb(%s)\n", col[i], str);
	}
	DestroyPixelWand(pix);
	return 0;
}
