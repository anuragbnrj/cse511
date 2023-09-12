/*
 * Author: Anurag Banerjee
 * Creation Date: 09/03/2022
 * Description: CSE 511 - Assignment 1 - Create Movie Recommendation Database
 */

create table if not exists users (
	userid integer primary key,
	name text not null
);

create table if not exists movies (
	movieid integer primary key,
	title text not null
);

create table if not exists taginfo (
	tagid integer primary key,
	content text not null
);

create table if not exists genres (
	genreid integer primary key,
	name text not null
);

create table if not exists ratings (
	userid integer not null references users(userid) on
delete
	cascade,
	movieid integer not null references movies(movieid) on
	delete
		cascade,
		rating numeric not null check(rating >= 0.0
			and rating <= 5.0),
		timestamp bigint not null,
		primary key(userid,
		movieid)
);

create table if not exists tags (
	userid integer references users(userid) on
delete
	cascade,
	movieid integer references movies(movieid) on
	delete
		cascade,
		tagid integer references taginfo(tagid) on
		delete
			cascade,
			timestamp bigint not null,
			primary key(userid,
			movieid,
			tagid)
);

create table if not exists hasagenre (
	movieid integer not null references movies(movieid) on
delete
	cascade,
	genreid integer not null references genres(genreid) on
	delete
		cascade,
		primary key(movieid,
		genreid)	
);
