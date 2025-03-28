import tracemalloc

tracemalloc.start()

# Код, который анализируем
data = [1] * 100000

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

for stat in top_stats[:5]:
    print(stat)