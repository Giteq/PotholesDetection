#define uint8_t	unsigned char

#define uint16_t unsigned short int

#define int16_t short int

class Accelerometer
{
public:
	/**
	 * Measurment type.
	 * */
	enum meauserment_type
	{
		BYPASS_MODE = 0u,
		FIFO_MODE = 1u,
		STREAM_MODE = 2u,
		STREAM_TO_FIFO_MODE = 3u,
		BYPASS_TO_STREAM_MODE = 4u,
		DYNAMIC_STREAM_MODE = 6u,
		BYPASS_TO_FIFO_MODE = 7u
	};
	
	/**
	 *  Default values of control registers.
	 **/
	enum ctrl_registers_default
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

	/**
	 *  Register addresses.
	 **/
	enum reg_addr
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
	
	/**
	 * Accelerometer class constructor. 
	 * Initialize I2C communication and control registers of acc.
	 * Note: This function sets default I2C address to 0x6B.
	 *
	 * @return		 
	 **/
	Accelerometer();
	
	/**
	 * Accelerometer class constructor. 
	 * Initialize I2C communication and control registers of acc.
	 * 
	 * @param		i2c_address -> I2C address to be set.
	 *
	 * @return		 
	 **/
	Accelerometer(uint8_t i2c_address);
	
	/**
	 * Function returns actual value of each axis (x, y and z)
	 * Note: Function returns 16bit integer. Host should procces this to G value.
	 * 
	 * @param		all_axis	Returned buffer with each axis actual value.
	 * 
	 * @return		 
	 **/
	void measure(int16_t *all_axis);
	
	/**
	 * Function turns off accelerometer.
	 *
	 * @return		 
	 **/
	void turn_off();
	
private:
	int16_t fd;
	uint8_t i2c_address;

	/**
	 * Function writes value to the accelerometer's register.
	 *
	 * @param address			Register address.
	 * @param value				Value to be write.
	 * 
	 * @return		 			Error code.
	 **/
	int write_reg(uint8_t address, uint8_t value);
	
	
	/**
	 * Function reads value from the accelerometer's register.
	 *
	 * @param address			Register address.
	 * 
	 * @return		 			Read value.
	 **/
	int read_reg(int address);
	
	/**
	 * Function turns on accelerometer.
	 * 
	 * @return		 			Error code.
	 **/
	int turn_on();
	
	/**
	 * Function cheks if accelerometer is  on.
	 * 
	 * @return		 			true->acc on, false->acc off
	 **/
	bool is_on();
};
