#!/usr/bin/python2.7
#
# Assignment2 Interface
#

import psycopg2
import os
import sys


# Donot close the connection inside this file i.e. do not perform openconnection.close()
def RangeQuery(ratingsTableName, ratingMinValue, ratingMaxValue, openconnection):
    required_ratings = []

    rrobin_ratings_meta_table = "RoundRobinRatingsMetadata"
    rrobin_partition_table_prefix = "RoundRobinRatingsPart"

    rrobin_partition_numbers_query = "select partitionnum from {table_name};".format(
        table_name=rrobin_ratings_meta_table
    )

    rrobin_partition_select_query = "select * from {rrobin_partition_table_prefix}{partition_number} where rating>={rating_min_value} and rating<={rating_max_value};"

    with openconnection.cursor() as cursor:
        cursor.execute(rrobin_partition_numbers_query)
        rrobin_number_of_partitions = cursor.fetchone()[0]

        for partition_number in range(0, rrobin_number_of_partitions):
            cursor.execute(
                rrobin_partition_select_query.format(
                    rrobin_partition_table_prefix=rrobin_partition_table_prefix,
                    partition_number=partition_number,
                    rating_min_value=ratingMinValue,
                    rating_max_value=ratingMaxValue
                )
            )
            ratings = cursor.fetchall()
            for rating in ratings:
                rating = list(rating)
                rating.insert(
                    0,
                    "{rrobin_partition_table_prefix}{partition_number}".format(
                        rrobin_partition_table_prefix=rrobin_partition_table_prefix,
                        partition_number=partition_number
                    )
                )
                required_ratings.append(rating)

    range_ratings_meta_table = "RangeRatingsMetadata"
    range_partition_table_prefix = "RangeRatingsPart"

    range_partition_numbers_query = "select partitionnum from {table_name} where maxrating>={rating_min_value} and minrating<={rating_max_value};".format(
        table_name=range_ratings_meta_table,
        rating_min_value=ratingMinValue,
        rating_max_value=ratingMaxValue
    )

    range_partition_select_query = "select * from {range_partition_table_prefix}{partition_number} where rating>={rating_min_value} and rating<={rating_max_value};"

    with openconnection.cursor() as cursor:
        cursor.execute(range_partition_numbers_query)
        rows = cursor.fetchall()
        partition_numbers = []
        for row in rows:
            partition_numbers.append(row[0])
        for partition_number in partition_numbers:
            cursor.execute(
                range_partition_select_query.format(
                    range_partition_table_prefix=range_partition_table_prefix,
                    partition_number=partition_number,
                    rating_min_value=ratingMinValue,
                    rating_max_value=ratingMaxValue
                )
            )
            ratings = cursor.fetchall()
            for rating in ratings:
                rating = list(rating)
                rating.insert(
                    0,
                    "{range_partition_table_prefix}{partition_number}".format(
                        range_partition_table_prefix=range_partition_table_prefix,
                        partition_number=partition_number
                    )
                )
                required_ratings.append(rating)

    writeToFile("RangeQueryOut.txt", required_ratings)


def PointQuery(ratingsTableName, ratingValue, openconnection):
    required_ratings = []

    rrobin_ratings_meta_table = "RoundRobinRatingsMetadata"
    rrobin_partition_table_prefix = "RoundRobinRatingsPart"

    rrobin_partition_numbers_query = "select partitionnum from {table_name};".format(
        table_name=rrobin_ratings_meta_table
    )

    rrobin_partition_select_query = "select * from {rrobin_partition_table_prefix}{partition_number} where rating={rating_value};"

    with openconnection.cursor() as cursor:
        cursor.execute(rrobin_partition_numbers_query)
        rrobin_number_of_partitions = cursor.fetchone()[0]

        for partition_number in range(0, rrobin_number_of_partitions):
            cursor.execute(
                rrobin_partition_select_query.format(
                    rrobin_partition_table_prefix=rrobin_partition_table_prefix,
                    partition_number=partition_number,
                    rating_value=ratingValue
                )
            )
            ratings = cursor.fetchall()
            for rating in ratings:
                rating = list(rating)
                rating.insert(
                    0,
                    "{rrobin_partition_table_prefix}{partition_number}".format(
                        rrobin_partition_table_prefix=rrobin_partition_table_prefix,
                        partition_number=partition_number
                    )
                )
                required_ratings.append(rating)

    range_ratings_meta_table = "RangeRatingsMetadata"
    range_partition_table_prefix = "RangeRatingsPart"

    range_partition_numbers_query = "select partitionnum from {table_name} where maxrating>={rating_value} and minrating<={rating_value};".format(
        table_name=range_ratings_meta_table,
        rating_value=ratingValue
    )

    range_partition_select_query = "select * from {range_partition_table_prefix}{partition_number} where rating={rating_value};"

    with openconnection.cursor() as cursor:
        cursor.execute(range_partition_numbers_query)
        rows = cursor.fetchall()
        partition_numbers = []
        for row in rows:
            partition_numbers.append(row[0])
        for partition_number in partition_numbers:
            cursor.execute(
                range_partition_select_query.format(
                    range_partition_table_prefix=range_partition_table_prefix,
                    partition_number=partition_number,
                    rating_value=ratingValue
                )
            )
            ratings = cursor.fetchall()
            for rating in ratings:
                rating = list(rating)
                rating.insert(
                    0,
                    "{range_partition_table_prefix}{partition_number}".format(
                        range_partition_table_prefix=range_partition_table_prefix,
                        partition_number=partition_number
                    )
                )
                required_ratings.append(rating)

    writeToFile("PointQueryOut.txt", required_ratings)


def writeToFile(filename, rows):
    f = open(filename, 'w')
    for line in rows:
        f.write(','.join(str(s) for s in line))
        f.write('\n')
    f.close()
