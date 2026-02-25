
#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Использование: $0 <путь_к_папке> <права_доступа>"
    exit 1
fi

DIRECTORY=$1
PERMISSIONS=$2

if [ ! -d "$DIRECTORY" ]; then
    echo "Данной папки нет"
    exit 1
fi

find "$DIRECTORY" -type f -perm "$PERMISSIONS" > result.txt

echo "Результаты сохранены в result.txt"
