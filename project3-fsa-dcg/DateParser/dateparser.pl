/*
	Master in Artificial Intelligence
	Natural Language Processing
	Javier Fernandez
	Alejandro Hernandez

--------------------------------------------
Date parsing with definite clause grammars
--------------------------------------------

*/

/*
----------------------------------------------------------------
 Helper predicates for building a complete DCG for date matching
----------------------------------------------------------------
*/

/*
 Defining general regular expression operators
 The following expressions allow to use the operators
 without parenthesis
*/

:- op(100,xf,+).
:- op(100, xf, ?).
:- op(100, xf, *).
:- op(100, xf, .).

/* One or more occurrences of expression*/
+(E) --> E.
+(E) --> E,+(E).

/*One or none ocurrences of expression*/
?(_) --> [].
?(E) --> E.

/*None or any occurences of expression*/
*(_) --> [].
*(E) --> E, *(E).

/* Exactly one ocurrence */
.(E) --> E.

/* birthday - valid atom*/
birthdate --> ("birth_date" | "birth date").

/*month in letters */
month_letters --> ("January" | "january" | "February" | "february" | "March" | "march" | 
"April" | "april" | "May" | "may" | "June" | "june" | "July" | "july" | "August" | "august" 
| "September" | "september" | "October" | "october" | "November" | "november" | "December" | "december").

/*month in letters short*/
month_letters_short --> ("Jan" | "Feb" | "Mar" | "Apr" 
| "May" | "Jun" | "Jul" | "Aug" | "Sep" | "Oct" | "Nov" | "Dec").

month_num --> digit.
month_num --> "0",digit_non0;"10";"11";"12".

month --> month_num;month_letters;month_letters_short.

/* Special delimiters */
space --> " ".
tab --> "\t".
comma --> ",".

/* years matcher */
year --> ?(cyears),?(digit),?(digit),?(digit),digit.
	
/* Matches any digit*/	
isDigit(D) -->
        [D],
        { code_type(D, digit)}.

/* recreates any of the decimals digits */
digit_non0 --> "1";"2";"3";"4";"5";"6";"7";"8";"9".
digit --> "0";digit_non0.

/* Match a digit between 1 and 31*/
day(X)--> {
	number_codes(Y,X),
	Y > 0, Y < 32
}.

day --> digit.
day --> "0",digit;"1",digit;"2",digit;"30";"31".

/* Matches a week day*/
week_day --> "Monday";"monday";"Tuesday";"tuesday";"Wednesday";"wednesday";"Thursday";"thursday";"Friday";"friday";"Saturday";"saturday";"Sunday";"sunday".

/* brackets*/
o_brackets --> "[[".
c_brackets --> "]]".

/* bars */
bar --> "|".

end_trash --> space;".".

/* dash */
dash --> "-".

/* comma */
comma -->",".

/* dot */
dot --> ".".

/* year special previous text */
cyears --> "c.".

/* unknown */
unknown --> "unknown";"Unknown".

/* or */
ortext --> "or".

/* day termination */
day_termination --> "th";"st";"nd";"rd".

/* trash */
trash --> letters;dash;"<";"!";">";"(";")";"|";dot;comma;space;digit.

pretext --> "about";"Date?";"born";cyears;"ca".

/*
 All leters for trash match
*/
letters -->"a";"A";"b";"B";"c";"C";"d";"D";"e";"E";"f";"F";"g";"G";"h";"H";"i";"I";"j";"J";"k";"K";"l";"L";"m";"M";"n";"N";"o";"O";"p";"P";"q";"Q";"r";"R";"s";"S";"t";"T";"u";"U";"v";"V";"x";"X";"y";"Y";"z";"Z".

/*
------------------------------------
 File parser
------------------------------------
*/

:- use_module(library(pio)).

lines([]) --> call(eos),!.
lines([Line|Lines]) --> line(Line), lines(Lines).

eos([], []).

line([])  --> ( "\n" ; call(eos) ), !.
line([L|Ls]) --> [L], line(Ls).

/*
------------------------------------
 Date parsing and matching grammars
------------------------------------
*/

/* match month, year */
matchphrase --> birthdate,tab,?(o_brackets),month,space,day,?(c_brackets),?(comma),?(space),?(o_brackets),year,?(c_brackets).

/* match day, month, year */
matchphrase --> birthdate,tab,?(o_brackets),day,space,month,?(c_brackets),?(comma),?(space),?(o_brackets),year,?(c_brackets).

/* match year */
matchphrase --> birthdate,tab,?(pretext),?(space),?(o_brackets),year,?(c_brackets).

/* match year, month, day */
matchphrase --> birthdate,tab,?(o_brackets),year,bar,month,bar,day,?(c_brackets),?(end_trash).


/*
------------------------------------
 Special cases matcher
------------------------------------
*/

/* 
Match cases as birth_date	[[October]] [[1977]]
*/
matchphrase --> birthdate,tab,o_brackets,month,c_brackets,space,o_brackets,year,c_brackets.

/* 
Match cases as 
birth_date	[[1901-09-27]]
birth_date	[[1901-Sep-27]]
birth_date	[[1901-September-27]]
*/
matchphrase --> birthdate,tab,o_brackets,year,dash,month,dash,day,c_brackets.

/*
Match cases as 
birth_date	[[November  21]], [[1968]]
birth_date	[[November 21]], [[1968]]
birth_date	[[November 21]],[[1968]]
birth_date	[[Nov  21]], [[1968]]
birth_date	[[February 4th]], [[1923]]
birth_date	[[13 November]], [[1943]]
*/
matchphrase --> birthdate,tab,o_brackets,month,space,?(space),day,?(day_termination),?(space),c_brackets,comma,?(space),o_brackets,year,c_brackets.
matchphrase --> birthdate,tab,o_brackets,day,?(day_termination),space,?(space),month,?(space),c_brackets,comma,?(space),o_brackets,year,c_brackets.

/*
Match cases as 
birth_date	Monday, [[December 19]], [[1955]]
birth_date	Monday, [[19 December]], [[1955]]
*/
matchphrase --> birthdate,tab,?(o_brackets),week_day,?(c_brackets),?(comma),space,o_brackets,month,space,?(space),day,?(space),c_brackets,?(comma),?(space),o_brackets,year,c_brackets.

matchphrase --> birthdate,tab,?(o_brackets),week_day,?(c_brackets),?(comma),space,o_brackets,day,space,?(space),month,?(space),c_brackets,?(comma),?(space),o_brackets,year,c_brackets.

/*
Match cases as 
birth_date	Unknown
birth_date	unknown
*/
matchphrase --> birthdate,tab,unknown.

/*
Match cases as 
birth_date	Unknown
birth_date	unknown
*/
matchphrase --> birthdate,tab,unknown.

/*
Match cases as 
birth_date	1302 or 1303
birth_date	[[626]] or [[627]]
birth_date	[[February 2]], [[1650]] or [[1651]]
*/
matchphrase --> birthdate,tab,?(o_brackets),year,?(c_brackets),space,ortext,space,?(o_brackets),year,?(c_brackets).

matchphrase --> birthdate,tab,?(o_brackets),?(month),?(space),?(day),?(c_brackets),?(o_brackets),year,?(c_brackets),space,ortext,space,?(o_brackets),year,?(c_brackets).
/*
Match cases as 
birth_date	July, [[1980]]
*/
matchphrase --> birthdate,tab,month,comma,space,o_brackets,year,c_brackets.

/*
Match cases as 
birth_date	January [[1968]]
*/
matchphrase --> birthdate,tab,month,space,o_brackets,year,c_brackets.

/*
Match cases as 
birth_date	26th April 1951
birth_date	26th April, 1951
*/
matchphrase --> birthdate,tab,day,day_termination,space,month,?(comma),space,year.

/*
Match cases as 
birth_date	[[13 September]] , [[1973]]
birth_date	[[13 September]], [[1973]]
birth_date	[[13 September]] [[1973]]
*/
matchphrase --> birthdate,tab,o_brackets,day,space,month,?(space),c_brackets,?(space),?(comma),?(space),o_brackets,year,c_brackets.

/*
birth_date	[[June]], [[1763]]
birth_date	June, 1763
*/
matchphrase --> birthdate,tab,?(o_brackets),month,?(space),?(c_brackets),?(space),?(comma),?(space),?(o_brackets),year,?(c_brackets).

/*
Match cases as
birth_date	[[August 8]]
birth_date	October 1
*/
matchphrase --> birthdate,tab,?(o_brackets),month,space,day,?(c_brackets).

/*
Match cases as
birth_date	[[April 14]],
birth_date	[[April 14]]
*/
matchphrase --> birthdate,tab,?(o_brackets),month,space,day,?(c_brackets),?(comma).

/*
Match cases as
birth_date	[[july 18]], [[1949]]
birth_date	[[May 13]]. [[1928]]
*/
matchphrase --> birthdate,tab,?(o_brackets),month,space,day,?(c_brackets),?(comma | dot),?(space),?(o_brackets),year,?(c_brackets).

/*
Match cases as
birth_date	[[September]] [[11]], [[1981]
*/
matchphrase --> birthdate,tab,?(o_brackets),month,?(c_brackets),?(comma | dot),?(space),?(o_brackets),day,?(c_brackets),?(comma | dot),?(space),?(o_brackets),year,?(c_brackets).
/*

 Allowing matchphrase to match trash content after correct date parsed
*/
fmatchphrase --> matchphrase,*(trash).


/* 
   Process a string as char list H by increasing Accum
   if matchphrase is true and continuing otherwise.
   Total counts the total number of phrases evaluated.

*/
parse(H,Total, Accum,X, NewTotal):-
	phrase(fmatchphrase,H), X is Accum+1, NewTotal is Total+1;
	\+ phrase(fmatchphrase,H), X is Accum, NewTotal is Total+1, writef(H), nl.
	

main :- phrase_from_file(lines(Ls), './examples.txt'),
	match_dates(Ls,0,0).
	
match_dates([H|T],Total,Accum):- parse(H,Total,Accum,X,NewTotal),match_dates(T,NewTotal,X).
match_dates([],Total, X):- Y is X/Total, write(Total),nl, write(X),nl,write(Y).

	







    