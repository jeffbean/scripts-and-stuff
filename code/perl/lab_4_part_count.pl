#! /usr/bin/perl -w
use strict;


my $line_count = 0;
my $char_count = 0;
my $word_count = 0;
my $total_words;
my $total_chars;
my $flag = 0;
print "File\t\tCharacters\t\tWords\t\tLines\n";
while (<>) {
	my @x = "$_";

    foreach my $a (@x) {
    		my @w = split(/ /, $a);
 
    		foreach my $a (@w) {
    				my @h = split(//, $a);
    				foreach (@h) {
    					$char_count++;
    					$total_chars++;
    				}
    				$word_count++;
    				$total_words++;
    		}
    		$line_count++;
    }

} continue {
	print "$ARGV \t$char_count \t\t\t$word_count\t\t$line_count\n" if eof;
	$word_count =0 if eof;
	$line_count =0 if eof;
	$char_count =0 if eof;

}
print "Total\t\t$total_chars\t\t\t$total_words\t\t$.\n";
