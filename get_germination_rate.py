def count_germination_rate(filename):
    ''' Расчет всхожести '''
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
            # Удаляем потенциальные пустые строки
            lines = [line for line in lines if line]

            if lines:
                germinated_seeds = len(lines) - 1

                # Обработка последней строки
                last_line = lines[-1]
                if last_line.endswith('=0'):
                    try:
                        ungerminated_seeds = int(last_line.split('=')[0])
                    except Exception as e:
                        print(
                            f"Ошибка {e} в формате последней  "
                            f"строки файла {filename}: {last_line}"
                        )
                germination_rate = (
                    germinated_seeds/(ungerminated_seeds + germinated_seeds)
                )

    except Exception as e:
        print(f"Ошибка при чтении файла {filename} " + e)

    finally:
        return germination_rate