from path_mgmt import add_corteva_to_path
add_corteva_to_path()

from sqlalchemy.exc import IntegrityError

from corteva_app.database.mgmt import db_session

if __name__ == "__main__":

    # Using an ORM for complex subqueries such as this would be a pain. Instead we will directly execute SQL

    sql_text = """
    insert into weather_stats
    (year, station_id, avg_max_temp, avg_min_temp, total_precip)

    with all_stats as (
    select 
        extract(year from weather.date)::int as year, 
        station_id, 
        avg(max_temp) as avg_max_temp, 
        avg(min_temp) as avg_min_temp, 
        sum(precip) as total_precip,
        -- count will not include NULL values, use this to determine which year/station combos have complete data
        count(max_temp) as nnull_max_temp,
        count(min_temp) as nnull_min_temp,
        count(precip) as nnull_precip
    from public.weather
    group by station_id, year
    -- sometimes stations only have data for part of the year - we only want summary stats if the station has data for every day of the year
    -- otherwise our data is not normalized and we would draw incorrect conclusions on data biased towards certain seasons
    -- even worse, the bias would be different for each station/year combination
    )
    -- further filter the subquery to remove values where the dataset is not complete
    -- in this case it is not complete if it has fewer than 365 days
    -- sometimes a station will have complete temp records, but not complete precip records, and vice versa
    select 
        year,
        station_id,
        case when nnull_max_temp < 365 then null else avg_max_temp end,
        case when nnull_min_temp < 365 then null else avg_min_temp end,
        case when nnull_precip < 365 then null else total_precip end
    from all_stats
    ;
    """

    count_query = """
    select count(*) from weather_stats;
    """

    try:
        # run the analysis and populate the weather_stats table with the result
        result = db_session.execute(sql_text)
        # count number of rows we inserted
        count_result = db_session.execute(count_query).fetchall()
        # unnest the result since count_result is a generator
        count: int = [row[0] for row in count_result][0]
        print(f"Added {count} rows into weather_stats")
    except IntegrityError as e:
        print(e, "\n")
        print("weather_stats table has already been populated with results")
