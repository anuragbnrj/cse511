/*
 * Author: Anurag Banerjee
 * Creation Date: 09/12/2022
 * Description: CSE 511 - Assignment 2 - SQL Query for Movie Recommendation
 */


-- Query 1 --
create table query1 as
select
	g."name" as "name",
	count(g."name") as moviecount
from
	genres g,
	hasagenre h
where
	g.genreid = h.genreid
group by
	g."name";


-- Query 2 --
create table query2 as
select
	g."name" as "name",
	avg(r.rating) as rating
from
	genres g,
	hasagenre h,
	ratings r
where
	g.genreid = h.genreid
	and h.movieid = r.movieid
group by
	g."name";


-- Query 3 --
create table query3 as
select
	m.title as title,
	count(m.movieid) as countofratings
from
	movies m,
	ratings r
where
	m.movieid = r.movieid
group by
	m.movieid;


-- Query 4 --
create table query4 as
select
	m.movieid as movieid,
	m.title as title
from
	movies m,
	hasagenre h,
	genres g
where
	m.movieid = h.movieid
	and h.genreid = g.genreid
	and g."name" = 'Comedy';


-- Query 5 --
create table query5 as
select
	m.title as title,
	avg(r.rating) as average
from
	movies m,
	ratings r
where
	m.movieid = r.movieid
group by
	m.movieid;


-- Query 6 --
create table query6 as
select
	avg(r.rating) as average
from
	genres g,
	hasagenre h,
	ratings r
where
	g.genreid = h.genreid
	and h.movieid = r.movieid
	and g."name" = 'Comedy'
group by
	g."name";


-- Query 7 --
create table query7 as
select
	avg(r.rating)
from
	genres g,
	hasagenre h,
	ratings r
where
	g.genreid = h.genreid
	and h.movieid = r.movieid
	and g."name" = 'Comedy'
	and r.movieid in (
	select
		r2.movieid
	from
		genres g2,
		hasagenre h2,
		ratings r2
	where
		g2.genreid = h2.genreid
		and h2.movieid = r2.movieid
		and g2."name" = 'Romance')
group by
	g."name";


-- Query 8 --
create table query8 as
select
	avg(r.rating)
from
	genres g,
	hasagenre h,
	ratings r
where
	g.genreid = h.genreid
	and h.movieid = r.movieid
	and g."name" = 'Romance'
	and r.movieid not in (
	select
		r2.movieid
	from
		genres g2,
		hasagenre h2,
		ratings r2
	where
		g2.genreid = h2.genreid
		and h2.movieid = r2.movieid
		and g2."name" = 'Comedy')
group by
	g."name";


-- Query 9 --
create table query9 as
select
	r.movieid as movieid,
	r.rating as rating
from
	ratings r
where
	userid = :v1;	

