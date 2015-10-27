#! /usr/bin/perl -w
use strict;

my @x = <STDIN>;
my $line_count = 0;
my $word_count = 0;
my %hah;

foreach my $a (@x) {
		my @w = split(/[\n\t\s]+/, $a);
		
		foreach my $p (@w) {
			if (exists($hah{ $p })){
				$hah{ $p } = $hah{ $p } + 1;
			}
			else{
				$hah{ $p } = 1;
			}
		}
		$line_count++;
}
my @all_words = keys(%hah);
foreach (@all_words){
	print "<$_> appered $hah{$_} times.\n";
}
