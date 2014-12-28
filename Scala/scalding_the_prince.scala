/**

This file downloads text from Machiavelli's The Prince and undertakes a word count, pulling the top 50 most frequent words. 

It is similar to johnynek's scalding_alice.scala tutorial, available at https://gist.github.com/johnynek/a47699caa62f4f38a3e2 , 
which undertakes a word count analysis of Alice in Wonderland.


To run:

 git clone https://github.com/twitter/scalding.git
 cd scalding
 ./sbt scalding-repl/console
*/

import scala.io.Source
import com.twitter.scalding._




val prince = Source.fromURL("https://www.gutenberg.org/files/1232/1232.txt").getLines

val princeLineNum = prince.zipWithIndex.toList

val princePipe = TypedPipe.from(princeLineNum)

val princeWordList = princePipe.map { line => line._1.split("\\s+").toList }
 
val princeWords = princeWordList.flatten

val princeWithCount = princeWords.map { word => (word, 1L)}

val princeWordCount = princeWithCount.group.sum

princeWordCount.dump

val princeTop50 = princeWordCount
.groupAll
.sortBy { case (word , count) => -count}
.take(50)
//prince is the 50th most common word in The Prince, with 50 repetitions

//Last line on which each word appears?
val princeWordLine = princePipe.flatMap { case (text, line) =>
	text.split("\\s+").toList.map { word => (word, line)}
	}

val princeLastLine = princeWordCount.filter { case (word, _ ) => word == 'prince}

val princeLastLine = princeWordLine.group.max

val princeWordLastLine = princeLastLine.filter { case (word, _ ) => word == 'prince}
