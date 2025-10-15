#!/bin/bash
echo "Usuario $(whoami)"
echo "Python: $(which python3)"
for i in $(seq 1 5); do
  sleep 2
  python cliente.py < /dev/null &
done


wait
echo "Todos los procesos finalizados."
