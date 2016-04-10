Performance Comparison between NoSQL and SQL
============================================

> [浏览中文翻译](README-zh.md)

## 0x00 Introduced: How to Category Data

With the rapid development of information society, the increasing data impact on people's traditional data processing technology, with more and more chaotic and more massive real-time data changing people's lives. Processing technology of information has become a new problem. In simple terms, we can roughly divide data into three broad categories.

+ The information which can be represented by unified structure, called structured data, such as numbers, symbols;

+ More miscellaneous information, which can not use numbers or unified structure represented, such as text, images, sound, web pages. We call these information unstructured data.

+ The data between structured information and unstructured data, which we call semi-structured data. More detailed, even though semi-structured data then has fields, but the field may be able to expand. It means the number of fields is variable. semi-structured data can be regarded as the gray transition zone between structured data and unstructured one.

## 0x01 The Dominator: SQL

At the beginning of the information society, people are only able to handle very simple everyday data, such as students' report cards, staff's pay slips. Such information, which is called ___structured data___ . After exploring a long period of time, people's awareness of the database has gone through three stages including the layered database, the network database and the relational database. Ultimately, as a representative of a relational database, SQL, has been widely used and promoted, has become a powerful structured database.

Structured data, because of its remarkable structural features, can easily be expressed by the relationship of the actual information abstraction using two-dimensional table. Furthermore, the tables that is connected with each other could express a more complex relationship. SQL undoubtedly powers the relational database to the extreme.

## 0x02 Amazing defier: NoSQL

With the increasing computer power, people has been creating more and more digital ___unstructured data___ . The complexity and amount of data also geometrically increased. Similarly, with the arrival of the era of Web 2.0, data redundancy and irregularities are constantly increasing. Man has discovered, surprisingly, data has became more and more difficult to be structured, or it may be unattainable. At this time, based on the concept of Key-Value, unstructured database has been created. It was then, when NoSQL started coming into sight.

Efficient handling of unstructured data, perfect performance on concurrent using, strong support of real-time data upgrading, all in all, makes NoSQL constantly has a larger market, with the impact on SQL's solid position for many years .

## 0x03 Of Swords, New Challenge

From an early age when people improved SQL relational databases, to the eighties when men proposed a conceptual model of NoSQL,  then to today's Web 2.0 era, people are finally beginning to realize the development of database technology has lagged far behind the growth of data. Meanwhile, NoSQL stared to impact on SQL database's dominant position.

___On the one hand, NoSQL has a rapid processing capability on unstructured data; on the other hand, SQL‘s development means that the long-term stability and scalability is difficult for other models database to match___ .

Our project, is to compare various aspects of the two modes of database, and to analyze the pros and cons of both databases, for more in-depth study in the future.

### Environment

> OS：Ubuntu 14.0.2
>
> CPU:Intel(R) Core(TM) i5-4210M CPU @ 2.40GHZ
>
> SQL：MySQL-5.6.0
>
> NoSQL：MongoDB-2.4.9
>
> tool kit：MySQLslap，YCSB-0.7.0

### Experimental Program

We want to weigh the pros and cons of both databases, based on the mysql's and MongoDB's performance on different types of data.

> For SQL, we use SQL scripts to test it;
>
> For MongoDB, we use the JavaScript to test it;

Ultimately, we will present our results through a live demonstration and PowerPoint.

### Experimental content

+ Performance comparison based on structured data
  + Using existing data to test
  + Tested by the same database behavior
    + Query
    + Added Statement
    + Delete statement
    + Update statement
  + Performance tests' aspects
    + Responding Time
    + Footprint
    + Concurrency
    + Scalability  
+ Performance based on semi-structured data comparison
  + Using Web Crawler for HTML files to crawl and get semi-structured data sets
  + Performance testing results From the efficiency of recovering web page  
+ Performance comparison based on the completely unstructured data
