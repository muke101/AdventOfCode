#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#define MAXLINE 1000

int main()
{
	int c, i;
	int freq = 0;
	char number[MAXLINE]
	for (i=0; i<MAXLINE-1 && (c=getchar()) != EOF; ++i)
	{
		if (c != '\n' && isdigit(c))
		{
			number[i] = c;
		}
		else
		{
			if (c == '-')
			{
				
			}
			if (c == '\n')
			{
				freq = freq + atoi(number)
			}
		}
	}
	return 0;
}