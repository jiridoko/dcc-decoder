all:
	gcc -DTEST -pipe -g -W -Wall -c gertbot_pi_uart.c -o gertbot_pi_uart.o
	gcc -DTEST -pipe -g -W -Wall -c command.c -o command.o
	gcc -DTEST -g gertbot_pi_uart.o command.o -o test
	python3 setup.py build
	/bin/cp -f build/lib.linux-*/dcc.*.so ../dcc.so
clean:
	rm -rf *.so
	rm -rf *.o
	rm -rf build/
	rm -rf ./test

