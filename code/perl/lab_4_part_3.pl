#! /usr/bin/perl -w
use strict;
my $flag = 0;
$flag = 1 if ($ARGV[0] eq "-i");
shift(@ARGV) if ($ARGV[0] eq "-i");
open( PIPEOUT , "| perl -w lab_4_part_2-5.pl") or die ("Cant open script check current directory.");
open(PIPEIN, "perl -w lab_4_part_2-5.pl |") or die ("Cant open script check current directory.");

while(<>){
	$_ =~ tr/A-Z/a-z/ if ($flag);
 	print PIPEOUT "$_";
	my $line_of_input = <PIPEIN>;
	print "$line_of_input\n";
}

close(PIPEIN);
close(PIPEOUT);
