#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>



uint64_t msg[4] = {0x0001000100010001, 0x0001000100010001, 0x0001000100010001, 0x0001000100010001};
unsigned char * msg_p = (unsigned char *)msg;
uint64_t entropy[5] = {0};
uint64_t counter = 0;


void incr_msg()
{
	if (++msg[0] == 0)
	{
		if (++msg[1] == 0)
		{
			if (++msg[2] == 0)
			{
				if (++msg[3] == 0)
				{
					printf("Msg wrap around");
					exit(0);
				}
			}
		}		
	}
}

void print_status()
{
	int i;
	for (i=0 ; i<5 ; i++)
	{
		printf("Entropy%d = %016lX\n", i, entropy[i]);
	}
	printf("-------------------\n");
}

int get_entropy8b()
{
	int i, consec = 0, max_consec = 0;
	
	for (i=0 ; i<31 ; i++)
	{
		if (*(msg_p+i) == *(msg_p+i+1))
		{
			if (++consec > max_consec)
			{
				max_consec = consec;
			}
			
		}else
		{
			consec = 0;
		}
	}
	return max_consec;
}
int get_entropy16b()
{
	int i, consec = 0, max_consec = 0;
	uint8_t* p8 = msg_p;
	uint8_t* end_p = msg_p+30;
	
	while( p8 < end_p )
	{
		if (*(uint16_t*)p8 == *(uint16_t*)(p8+2))
		{
			if (++consec > max_consec)
			{
				max_consec = consec;
			}
			p8 += 2;
		}else
		{
			consec = 0;
			p8 += 1;
		}
	}
	return max_consec;
}
int main()
{
	int ret, ret2;
	
	while(1)
	{
		counter++;
		incr_msg();
		ret = get_entropy8b();
		ret2 = get_entropy16b();
		if (ret2>ret) ret = ret2;
		
		if (ret >=4)
		{
			entropy[4]++;
			if ( (entropy[4] & 0xFFFFFF) == 0)print_status();
		}
		else
		{
			entropy[ret]++;
			if ( (entropy[ret] & 0xFFFFFF) == 0)print_status();
		}
	}
}


