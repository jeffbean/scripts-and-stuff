#! /usr/bin/perl -w
use strict;

my @x = <STDIN>;
my $line_count = 0;
my $word_count = 0;
my %hah;
my $flag = 0;
$flag = 1 if ($ARGV[0] eq "-i");
foreach my $a (@x) {
		my @w = split(/[\n\t\s]+/, $a);
		
		foreach my $p (@w) {
		
			$p =~ tr/A-Z/a-z/ if ($flag);
			
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
