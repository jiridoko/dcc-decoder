#include <stdio.h>
#include <stdlib.h>
#include "gertbot_pi_uart.h"
#include "gertbot_defines.h"

#ifndef TEST
#include <Python.h>
#endif

void set_all_channels_to_dcc(int handle) {
	unsigned char message[5];
	for (unsigned char channel=0; channel<4; ++channel) {
		message[0] = CMD_START_VAL;
		message[1] = CMD_STOPSHORT;
		message[2] = channel;
		message[3] = ENDSTOP_OFF|ENB_ERR_IGNORE;
		message[4] = CMD_STOP_VAL;
		write_uart(handle, message,5);
	}

	for (unsigned char channel=0; channel<4; ++channel) {
		message[0] = CMD_START_VAL;
		message[1] = CMD_OPMODE;
		message[2] = channel;
		message[3] = MOT_MODE_DCC;
		message[4] = CMD_STOP_VAL;
		write_uart(handle, message,5);
	}
}

void dcc_config(int handle, unsigned char preamble, unsigned char repeat, unsigned char flags) {
	unsigned char message[10];
	message[0] = CMD_START_VAL;
	message[1] = CMD_DCC_CONFIG;
	message[2] = 0;
	message[3] = repeat;
	message[4] = preamble;
	message[5] = 0x00;
	message[6] = flags;
	message[7] = CMD_STOP_VAL;
	write_uart(handle, message,8);
}

int send_command(int handle, unsigned char count, unsigned char b1, unsigned char b2, unsigned char b3, unsigned char b4, unsigned char b5) {
	unsigned char message[10];
	message[0] = CMD_START_VAL;
	message[1] = CMD_DCC_MESS;
	message[2] = 0;
	message[3] = 0xF0 | count; //2 byte size
	message[4] = b1;
	message[5] = b2;
	message[6] = b3;
	message[7] = b4;
	message[8] = b5;
	message[9] = CMD_STOP_VAL;
	return write_uart(handle, message,10);
}

int init(int h) {
	int handle = open_uart(h);
	if (handle < 0) {
		printf("Failed to open uart\n");
		return -1;
	}

	set_all_channels_to_dcc(handle);
	dcc_config(handle, 16, 8, 0);
	printf("command.c-init(): returning handle %d\n", handle);
	return handle;
}

#ifndef TEST
static PyObject* dcc_init(PyObject* self, PyObject* args) {
	int handle;

	if (!PyArg_ParseTuple(args, "i", &handle))
		return NULL;

	int tmp = handle;
	handle = init(tmp);

	//Py_RETURN_NONE;
	return Py_BuildValue("i", handle);
}

static PyObject* dcc_send(PyObject* self, PyObject* args) {
	unsigned char handle, count, b1, b2, b3, b4, b5;

	if (!PyArg_ParseTuple(args, "bbbbbbb", &handle, &count, &b1, &b2, &b3, &b4, &b5))
		return NULL;

	printf("1234-handle: %d\n", handle);

	int ret = -1;
	ret = send_command(handle, count, b1, b2, b3, b4, b5);

	printf("1235-after-send_command-return: %d\n", ret);

	//Py_RETURN_NONE;
	return Py_BuildValue("i", ret);
}

static PyMethodDef DCCFunctions[] = {
	{"dcc_init", dcc_init, METH_VARARGS, "Initialize the DCC communication"},
	{"dcc_send", dcc_send, METH_VARARGS, "Send a DCC packet"},
	{NULL, NULL, 0, NULL}
};

static struct PyModuleDef DCCDefinition = {
	PyModuleDef_HEAD_INIT,
	"dcc",
	"DCC control package",
	-1,
	DCCFunctions
};

PyMODINIT_FUNC PyInit_dcc(void) {
	Py_Initialize();
	return PyModule_Create(&DCCDefinition);
}
#else
int main() {
	int handle = init(-1);

	send_command(handle, 2, 47, 130, 0, 0, 0);
	send_command(handle, 2, 47, 128, 0, 0, 0);

	close_uart(handle);

	return 0;
}
#endif
