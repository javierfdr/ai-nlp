/*
birth_date	[[1901-09-27]]
birth_date	[[December 13]], [[1952]]
birth_date	18 May, 1959
birth_date	[[March 25]], [[1968]]
birth_date	c. [[1412]]
birth_date	[[1877]]
*/

/* test digit*/
phrase(isDigit(X),"2"). /* X=2 */
phrase(isDigit(50),"2"). /* true */
phrase(isDigit(X),"21"). /* false */

/* test month num */
phrase(month_num(X),"12"). /* X=[49,50]*/
phrase(month_num([49,50]),"12"). /* true */

/* test years */
phrase(year,"1984"). /* true */
phrase(year,"984"). /* true */
phrase(year,"84"). /* true */
phrase(year,"4"). /* true */

/* test days */
phrase(day,"1"). /* true */
phrase(day,"21"). /* true */
phrase(day,"31"). /* true */
phrase(day,"32"). /* false */
 