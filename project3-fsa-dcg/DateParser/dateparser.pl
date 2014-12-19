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
month_letters --> ("January" | "February" | "March" | "April" 
| "May" | "June" | "July" | "August" | "September" 
| "October" | "November" | "December").

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
day --> "1",digit;"2",digit;"30";"31".

/* brackets*/
o_brackets --> "[[".
c_brackets --> "]]".

/* bars */
bar --> "|".

/* c for years*/
cyears --> "c.".

end_trash --> space;".".

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
/*
matchphrase --> birthdate,tab,month_letters,*(digit).
*/
matchphrase --> birthdate,tab,?(o_brackets),month,space,day,?(c_brackets),?(comma),?(space),?(o_brackets),year,?(c_brackets).

matchphrase --> birthdate,tab,?(o_brackets),day,space,month,?(c_brackets),?(comma),?(space),?(o_brackets),year,?(c_brackets).

matchphrase --> birthdate,tab,?(cyears),?(space),?(o_brackets),year,?(c_brackets).

matchphrase --> birthdate,tab,?(o_brackets),year,bar,month,bar,day,?(c_brackets),?(end_trash).

/* Match cases as 
birth_date	[[October]] [[1977]]
*/
matchphrase --> birthdate,tab,?(o_brackets),month,?(c_brackets),?(space),?(o_brackets),year,?(c_brackets).

/* Process a string as char list H by increasing Accum
   if matchphrase is true and continuing otherwise.
   Total counts the total number of phrases evaluated.

*/
parse(H,Total, Accum,X, NewTotal):-
	phrase(matchphrase,H), X is Accum+1, NewTotal is Total+1;
	\+ phrase(matchphrase,H), X is Accum, NewTotal is Total+1, writef(H).
	

main :- phrase_from_file(lines(Ls), '/Users/javierfdr/devel/mai/nlp-practice/repo/nlp/project3-fsa-dcg/DateParser/examples.txt'),
	match_dates(Ls,0,0).
	
match_dates([H|T],Total,Accum):- parse(H,Total,Accum,X,NewTotal),nl,match_dates(T,NewTotal,X).
match_dates([],Total, X):- Y is X/Total, write(Total),nl, write(X),nl,write(Y).

	







    