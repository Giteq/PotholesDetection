#define uint8_t	unsigned char

#define uint16_t unsigned short int

#define int16_t short int

enum acc_type_t
{	
ACC_1 = 0,
ACC_2	
};

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
		CTRL1_GYRO_DEFAULT = 0b11101111,
		CTRL0_DEFAULT = 0b01000000,
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

	
	enum acc_2_adr
	{
		FIFO_CTRL5 = 0xAu,
		CTRL1_XL = 0x10u,
		CTRL2_G = 0x11u,
		CTRL3_C = 0x12u,
		CTRL4_C = 0x13u,
		CTRL5_C = 0x14u,
		CTRL6_G = 0x15u,
		CTRL7_G = 0x16u,
		CTRL8_XL = 0x17u,
		CTRL9_XL = 0x18u,
		CTRL10_C = 0x19u,
		STATUS_REG = 0x1Eu
	};
	
	enum ctrl_registers_default_2
	{
		FIFO_CTRL5_DEFAULT = 0b01010110,
		CTRL1_XL_DEFAULT = 0b01010000,
		CTRL2_G_DEFAULT = 0b10000000
	};
	
	/**
	 *  Register addresses.
	 **/
	enum reg_addr
	{
		WHO_AM_I = 0x0Fu,
		CTRL0 = 0xF1u,
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
	
	enum
	{
		OUTX_L_G = 0x22u,
		OUTX_H_G = 0x23u,
		OUTY_L_G = 0x24u,
		OUTY_H_G = 0x25u,
		OUTZ_L_G = 0x26u,
		OUTZ_H_G = 0x27u,
		OUTX_L_XL = 0x28u,
		OUTX_H_XL = 0x29u,
		OUTY_L_XL = 0x2Au,
		OUTY_H_XL = 0x2Bu,
		OUTZ_L_XL = 0x2Cu,
		OUTZ_H_XL = 0x2Du
	};
	
	/**
	 * Accelerometer class constructor. 
	 * Initialize I2C communication and control registers of acc.
	 * Note: This function sets default I2C address to 0x6B.
	 *
	 * @return		 
	 **/
	Accelerometer();
	
	Accelerometer(int acc_type);
	
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
	 * Function returns value from WHO_AM_I register which reprezents type of Accelerometer.
	 * 
	 * @return		WHO_AM_I register value.
	 */
	uint8_t who_am_i(void);
	
	/**
	 * Function does self test. Checked in LSM6DS33.
	 * */
	int16_t self_test(void);
	
	/**
	 * Function turns off accelerometer.
	 *
	 * @return		 
	 **/
	void turn_off();
	
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
	
private:
	int16_t fd;
	uint8_t i2c_address;
	int acc_type;
	
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
