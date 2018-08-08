#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>
#include <time.h>
#include <unistd.h>

#define uint8_t	char

#define ACCELEROMETER_I2C_ADDR	0x6B

#define SELF_TEST_LEN	10  /* Time in seconds. */	

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
	FIFO_CTRL = 0x2E,	/* Register with mode cnfiguration. */
	FIFO_SRC = 0x2F, 	/* Register with informations about FIFO(s.43 datasheet). */
	OUT_X_L = 0x28,		/* Registers with x axis values. */
	OUT_X_H = 0x29,
	OUT_Y_L = 0x2A,		/* Registers with y axis values. */
	OUT_Y_H = 0x2B,
	OUT_Z_L = 0x2C,		/* Registers with z axis values. */
	OUT_Z_H = 0x2D
};

void write_reg(uint8_t address, uint8_t value)
{
	int fd;
	fd = wiringPiI2CSetup(ACCELEROMETER_I2C_ADDR);
	wiringPiI2CWriteReg8(fd, address, value);
}

int read_reg(int address, int print)
{
	int ret_val;
	int fd;
	fd = wiringPiI2CSetup(ACCELEROMETER_I2C_ADDR);
	ret_val = wiringPiI2CReadReg8(fd, address);
	
	if (print == 1)
	{
		std::cout << ret_val << std::endl;
	}
	
	return ret_val;
}

void turn_acc_on()
{
	int actual_value = read_reg(CTRL1, 0);
	
	/* Set 4 bit (Power mode). */
	actual_value |= 8;
	
	write_reg(CTRL1, actual_value);
	
}

void turn_acc_off()
{
	int actual_value = read_reg(CTRL1, 0);
	
	/* Clear 4 bit (Power mode). */
	actual_value &= 0xF7;
	
	write_reg(CTRL1, actual_value);
	
}

bool is_acc_on()
{
	bool ret_val = true;
	
	uint8_t ctrl1 = (uint8_t) read_reg(CTRL1, 0);
	
	/* Ceck if 4 bit (Power mode) is set. */
	if ( (ctrl1 | 0xF7) != 255)
	{
		/* If isn't return false. */
		ret_val = false;
	}
	
	return ret_val;
}	

bool imu_self_test()
{
	clock_t start = clock();
	clock_t stop = clock();
	while (stop - start <= SELF_TEST_LEN * CLOCKS_PER_SEC)
	{
		std::cout << "\nx";
		read_reg( OUT_X_L, 1 );
		std::cout << "\ny";
		read_reg( OUT_Y_L, 1 );
		std::cout << "\nz";
		read_reg( OUT_Z_L, 1 );
		sleep (1);	/* Delay for second. */
	}
}

