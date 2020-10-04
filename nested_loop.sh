# Use this sort of nested syntax to to call your python clli script
for batch_size in 16 32 128 256
do
    for amount in 1000 10000 10000
    do 
        python argparser.py --epochs=300 --batch_size=$batch_size --amount=$amount --learning_rate=1e-2
    done
done