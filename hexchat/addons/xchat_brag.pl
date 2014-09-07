#!/usr/bin/perl

######## Peer Kin Perl - HexChat - Brag - Power Script ########
######## 2013-02-23

# 2013-02-24 v1.6 Add pluraltext to pluralize or singularize final output
# 2013-02-24 v1.5 Add prefix2value sub
# 2013-02-24 v1.4 Don't count nicks that are joined to more than one channel shared with myself
# 2013-02-23 v1.3 Count only those nicknames that are equal or lesser in channel prefix power
# 2013-02-23 v1.2 Include all users
# 2013-02-23 v1.1 Include *owner !owner prefixes
# 2013-02-23 v1.0 Brag

use strict;
use warnings;

Xchat::register("PK Brag Script", "1.6", "PK Brag Script v1.6", "");
Xchat::hook_command("brag", \&brag);

sub brag {
        # Save context for later, so we can send our message to the active channel at the end of the script
        my $startcontext = Xchat::get_context();
        # Get an array of all channels
        my @channels = Xchat::get_list('channels');
        # Create a hash to keep our keyval counts
        my %powercount = (      networks => 0,
                                                channels => 0,
                                                users => 0,
                                                owner => 0,
                                                admin => 0,
                                                op => 0,
                                                hop => 0,
                                                voice => 0,
                                                regular => 0,
                                                kickable => 0,
                                                uniquenicks => 0,
    );

        ## Build an internal network-wide nickname list to      ##
        ## prevent adding nicknames more than once if they are  ##
        ## joined to more than one with us.                     ##
        my %NetNickList;

        # Iterate through each channel
        foreach my $chanitem (@channels){
                # Check type to see if it is a 1 => server window 2 => channel window 3 => dialog window
                my $chantype = $chanitem->{'type'};
                if ($chantype == 1) {
                        # This is a server window, add to network count
                        $powercount{'networks'}++;
                } elsif ($chantype == 2) {
                        # This is a channel window
                        $powercount{'channels'}++;
                        # Get channel name
                        my $chan = $chanitem->{'channel'};
                        # Set context for the following info commands to the chan
                        Xchat::set_context("$chan");

                        #### Calculate the number of owner|admin|op|hop|voice ####
                        # Get my user info on this channel
                        my $userinfo = Xchat::user_info();
                        # Grab user prefix for this channel to check if I am an op here
                        my $meprefix = $userinfo->{'prefix'};
                        # Grab only the first prefix character (highest power)
                        my $pwrprefix = substr $meprefix, 0, 1;
                        if ((defined $meprefix) && (length($meprefix) > 0)) {
                                # Map prefix to key
                                my %mapreplace = (      '+' => "voice",
                                                                        '%' => "hop",
                                                                        '@' => "op",
                                                                        '&' => "admin",
                                                                        '~' => "owner",
                                                                        '!' => "owner",
                                                                        '*' => "owner",
                                );
                                $pwrprefix =~ s/^([*!~&@%+])/$mapreplace{$1}/;
                        } else {
                                $pwrprefix = "regular";
                        }
                        # Increment hash based on mapped key
                        $powercount{$pwrprefix}++;

                        #### Calculate the total number of users I can kick   ####
                        # Get the array of users for the channel
                        my @Users = Xchat::get_list('users');
                        # Add the total number of users 
                        $powercount{'users'} += scalar(@Users);

                        #### Continue adding nicknames to the global nickname list ####
                        # Map prefixname to value
                        my $mynickvalue = prefix2value(substr $meprefix, 0, 1);
                        # Check each nickanme to see if we can kick it
                        my $netname = Xchat::get_info('network');
                        my $me = Xchat::get_info('nick');
                        foreach my $user (@Users) {
                                my $nickname = $user->{nick};
                                # Make sure I don't count myself
                                if ($nickname ne $me) {
                                        # Add the network+nickname to the global nickname list, if it is not alrealy in the list
                                        if (!exists($NetNickList{$netname.$nickname})) {
                                                $NetNickList{$netname.$nickname} = 0;
                                        }
                                        # Get their prefix value
                                        my $theirnickvalue = prefix2value(substr $user->{prefix}, 0, 1);
                                        # If I have a higher prefix, check off that this nick is kickable in at least one channel we share with them
                                        if ($theirnickvalue <= $mynickvalue) {
                                                $NetNickList{$netname.$nickname}++;
                                        }
                                }
                        }
                }
        }
        # Return context to active window
        Xchat::set_context("$startcontext");
        
        #### Calculate the total number of nicks in our global nickname list that I can kick with no repeats ####
        my @uniquenicks = keys(%NetNickList);
        foreach my $uniquenick (@uniquenicks) {
                $powercount{'uniquenicks'}++;
                if ($NetNickList{$uniquenick} > 0) {
                        $powercount{'kickable'}++;
                }
        }
                                
        my $outmsg = "I am currently on ".pluraltext($powercount{'channels'},"channel")." spanning ".pluraltext($powercount{'networks'},"network").". ";
        $outmsg .= "Somehow I have gotten myself ".pluraltext($powercount{'owner'},"owner").", ".pluraltext($powercount{'admin'},"admin").", ".pluraltext($powercount{'op'},"op").", ".pluraltext($powercount{'hop'},"halfop")." and ".pluraltext($powercount{'voice'},"voice").". ";
        $outmsg .= "I apparantly have \"power\" over $powercount{'kickable'}/$powercount{'users'} people ($powercount{'uniquenicks'} unique nicks). ";
        #$outmsg .= "If I did not check for repeat nicks, or my own nick, I would have assumed a total of $powercount{'users'} people. ";
        Xchat::command("say $outmsg");
        return Xchat::EAT_ALL;
}

sub prefix2value {
        # Map prefix character to value
        my $prefix = $_[0];
        if ((defined $prefix) && (length($prefix) > 0)) {
                my %valuemap = (        '+' => 2,
                                                        '%' => 3,
                                                        '%' => 4,
                                                        '@' => 5,
                                                        '&' => 6,
                                                        '~' => 7,
                                                        '!' => 8,
                                                        '*' => 9,
                );
                my $keyregex = join '', keys %valuemap;
                $prefix =~ s/^([$keyregex])/$valuemap{$1}/;
                return $prefix;
        } else {
                return 1;
        }
}

sub pluraltext {
        # Takes a number and a word without an 's' at the end
        # Returns the number and word, with or without an 's' if the word needs to be plural
        # Also returns 'no' instead of 0
        my ($X, $W) = @_;
        if ((!defined $X) || ($X < 1)) {
                return "no $W"."s";
        } elsif ($X == 1) {
                return "$X $W";
        } else {
                return "$X $W"."s";
        }
}

Xchat::print("PK Brag Script v1.6 loaded.");