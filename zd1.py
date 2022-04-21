#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import pathlib


def get_product(prds, name, shop, cost):
    """
    Добавить данные.
    """
    prds.append(
        {
            "name": name,
            "shop": shop,
            "cost": cost
        }
    )
    return prds


def display_products(products):
    if products:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Наименование товара",
                "Название магазина",
                "Стоимость"
            )
        )
        print(line)

        for idx, product in enumerate(products, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:<15} |'.format(
                    idx,
                    product.get('name', ''),
                    product.get('shop', ''),
                    product.get('cost', 0)
                )
            )
        print(line)

    else:
        print("Список продуктов пуст")


def save_products(file_name, prds):
    """
    Сохранить все записи в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(prds, fout, ensure_ascii=False, indent=4)


def load_products(file_name):
    """
    Загрузить все записи из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    """
    Главная функция программы
    """
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )
    parser = argparse.ArgumentParser("products")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new product"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The product`s name"
    )
    add.add_argument(
        "-s",
        "--shop",
        action="store",
        required=True,
        help="The shop that has the product"
    )
    add.add_argument(
        "-c",
        "--cost",
        action="store",
        required=True,
        help="The product`s cost"
    )
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all products"
    )

    args = parser.parse_args(command_line)
    destination = pathlib.Path.home() / args.filename
    is_dirty = False
    if destination.exists():
        products = load_products(destination)
    else:
        products = []

    if args.command == "add":
        products = get_product(
            products,
            args.name,
            args.shop,
            args.cost
        )
        is_dirty = True

    elif args.command == "display":
        display_products(products)

    if is_dirty:
        save_products(destination, products)


if __name__ == "__main__":
    main()