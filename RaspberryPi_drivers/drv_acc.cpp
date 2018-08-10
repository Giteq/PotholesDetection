#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>
#include <time.h>
#include <unistd.h>
#include "drv_acc.h"

#define uint8_t	char

#define ACCELEROMETER_I2C_ADDR	0x6B

#define SELF_TEST_LEN	10  /* Time in seconds. */	

struct splited_bits
{
		uint8_t b0 : 1;
		uint8_t b1 : 1;
		uint8_t b2 : 1;
		uint8_t b3 : 1;
		uint8_t b4 : 1;
		uint8_t b5 : 1;
		uint8_t b6 : 1;
		uint8_t b7 : 1;
};

union reg8
{
	splited_bits bits;
	uint8_t byte;
};

enum
{
	BYPASS_MODE = 0u,
	FIFO_MODE = 1u,
	STREAM_MODE = 2u,
	STREAM_TO_FIFO_MODE = 3u,
	BYPASS_TO_STREAM_MODE = 4u,
	DYNAMIC_STREAM_MODE = 6u,
	BYPASS_TO_FIFO_MODE = 7u
};

enum
{
	CTRL1 = 0x20,		/* Register with output data rate select, axis enable, power mode, and bandwidth selection. */
	CTRL2 = 0x21,
	CTRL3 = 0x0,		/* Interrupt disabled. */
	CTRL4 = 0x0,		/* Little Endian, scale -> 2. Rest default. */
	CTRL5 = 0x0, 		/* Default. */
	CTRL6 = 0x0,		/* Default. */
	FIFO_CTRL = 0x2E,	/* Register with mode cnfiguration. */
	FIFO_SRC = 0x2F, 	/* Register with informations about FIFO(s.43 datasheet). */
	OUT_X_L = 0x28,		/* Registers with x axis values. */
	OUT_X_H = 0x29,
	OUT_Y_L = 0x2A,		/* Registers with y axis values. */
	OUT_Y_H = 0x2B,
	OUT_Z_L = 0x2C,		/* Registers with z axis values. */
	OUT_Z_H = 0x2D
};

static int write_reg(uint8_t address, uint8_t value);

static int read_reg(int address);

static float acc_read_to_g(int acc_read);

void init_acc()
{
	
}

int turn_acc_on()
{
	int ret_val;
	
	int actual_value = read_reg(CTRL1);
	
	/* Set 4 bit (Power mode). */
	actual_value |= 8;
	
	ret_val = write_reg(CTRL1, actual_value);
	
	return ret_val;
	
}

void turn_acc_off()
{
	int actual_value = read_reg(CTRL1);
	
	/* Clear 4 bit (Power mode). */
	actual_value &= 0xF7;
	
	write_reg(CTRL1, actual_value);
	
}

bool is_acc_on()
{
	bool ret_val = true;
	
	uint8_t ctrl1 = (uint8_t) read_reg(CTRL1);
	
	/* Ceck if 4 bit (Power mode) is set. */
	if ( (ctrl1 | 0xF7) != 255)
	{
		/* If isn't return false. */
		ret_val = false;
	}
	
	return ret_val;
}	

void imu_self_test()
{
	reg8 ctrl2;
	
	
	
	ctrl2.byte = read_reg(CTRL2);
	ctrl2.bits.b1 = 1;		/* Set self test bit. */
	write_reg(CTRL2, ctrl2.byte);
	
	
	clock_t start = clock();
	clock_t stop = clock();
	while ((stop - start)/CLOCKS_PER_SEC <= SELF_TEST_LEN)
	{
		std::cout << "\nx";
		std::cout << float(acc_read_to_g(read_reg( OUT_X_L)));
		std::cout << "\ny";
		std::cout << float(acc_read_to_g(read_reg( OUT_Y_L)));
		std::cout << "\nz";
		std::cout << float(acc_read_to_g(read_reg( OUT_Z_L)));
		sleep (1);	/* Delay for second. */
	}
	
	ctrl2.bits.b1 = 0;		/* Clear self test bit. */
	write_reg(CTRL2, ctrl2.byte);
}

static float acc_read_to_g(int acc_read)
{
	float g_value;
	acc_read >>= 4u;		/* Drop 4 MSB bits. */
	
	g_value = acc_read / 1000;
	
	return g_value;
}

int write_reg(uint8_t address, uint8_t value)
{
	int ret_val;
	int fd;
	fd = wiringPiI2CSetup(ACCELEROMETER_I2C_ADDR);
	ret_val = wiringPiI2CWriteReg8(fd, address, value);
	
	return ret_val;
}

int read_reg(int address)
{
	int ret_val;
	int fd;
	fd = wiringPiI2CSetup(ACCELEROMETER_I2C_ADDR);
	ret_val = wiringPiI2CReadReg8(fd, address);
	
	
	return ret_val;
}
