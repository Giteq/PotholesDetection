#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>
#include <time.h>
#include <unistd.h>
#include "drv_acc.h"

#define ACCELEROMETER_I2C_ADDR	0x6B

#define SELF_TEST_LEN	10  /* Time in seconds. */	

/* Unique device identificator. */
#define ACC_IDENTIFICATOR 0b11010111

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

/* Default values of control registers. */
enum
{
	/* 800Hz, no Cut-off, normal mode, all axes enabled. */
	CTRL1_DEFAULT =  0b11101111,
	/* Not changed. */
	CTRL2_DEFAULT =  0,
	/* Not changed. */
	CTRL3_DEFAULT = 0,
	/* Not changed. NOTE:Full scale selection. */
	CTRL4_DEFAULT = 0,
	/* FIFO enable, NOTE: Out selection configuration. */
	CTRL5_DEFAULT = 0b01000000,
	/* FIFO mode select. */
	FIFO_CONTROL_DEFAULT = 0b00100000
};

enum
{
	WHO_AM_I = 0x0Fu,
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

static float acc_read_to_g(int acc_read);

static int ferq = 800; /*Frequency of measurment in Herz. */

static int fd;

void init_acc()
{
	fd = wiringPiI2CSetup(ACCELEROMETER_I2C_ADDR);
	write_reg(CTRL1, CTRL1_DEFAULT);
	write_reg(CTRL5, CTRL5_DEFAULT);
	write_reg(FIFO_CTRL, FIFO_CONTROL_DEFAULT);
	
	turn_acc_on();
}

void drv_acc_measure(uint16_t *all_axis)
{
	unsigned int x, y, z;
	x = (uint8_t)read_reg(OUT_X_L);
	x |= ((uint16_t)read_reg(OUT_X_H) << 8u);
	all_axis[0u] = x;
	y = (uint8_t)read_reg(OUT_Y_L);
	y |= ((uint16_t)read_reg(OUT_Y_H) << 8u);
	all_axis[1u] = y;
	z = (uint8_t)read_reg(OUT_Z_L);
	z |= ((uint16_t)read_reg(OUT_Z_H) << 8u);
	all_axis[2u] = z;
	
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
	ret_val = wiringPiI2CWriteReg8(fd, address, value);
	
	return ret_val;
}

int read_reg(int address)
{
	int ret_val;
	ret_val = wiringPiI2CReadReg8(fd, address);
	
	
	return ret_val;
}
