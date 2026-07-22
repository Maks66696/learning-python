def calculate_power(name, *base_stats, **items):
    print(f"Рассчёт для {name}")
    total_base = sum(base_stats)
    total_items = sum(items.values())
    return total_base, total_items


base_power, items_power = calculate_power("Hero", 10, 20, 30, sword = 15, ring = 5)
print(base_power, items_power)

