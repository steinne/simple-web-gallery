#!/usr/bin/perl
#use warnings;
use strict;

### configure to your location of albums, can be a full or relative path- 
### to control access through rw, place in a read/write area outside webpath.
my $rootDir = "/Library/WebServer/albums";

## albums are kept together, change the image and thumbnail directory names if need be.
my $albumImages = "Images";
my $thumbImages = "Thumbnails";

##  where the basic support images are located.  
## default is same directory as script.  Needs to be relative to script, or full path
my $supportImages = "."; 


my %FORM;
my %pFORM;
my $session_user;
my $user_name;
param_info();
my $login_error = "";
my $enter_check = "no";

my %users = (
	leah => 'seePics',
	melinda => 'seePics',
	judy => 'seePics',
	patricia => 'seePics',
	joanna => 'seePics',
	barbara => 'seePics',
	gerylyn => 'seePics',
	marybeth => 'seePics',
	kristine => 'stein',
	session_id => 'JhTTTgsNfdiKJSojaSDnsjdjYhsdbnqw67'
);

if ($FORM{'logout'}){
	my $past_time=gmtime(time()-600)." GMT";  
	my $cookie_session = "session_user=; path=/; expires=$past_time;";
	my $cookie_user = "user_name=; path=/; expires=$past_time;";
        print "Set-Cookie: " . $cookie_session . "\n";
        print "Set-Cookie: " . $cookie_user . "\n";
 	login_screen();    
	exit;
}


if ($users{$pFORM{'user'}} && ($pFORM{'password'} eq $users{$pFORM{'user'}})) {
	$enter_check = "yes";
}elsif ($ENV{'REQUEST_METHOD'} eq "POST"){
	$enter_check = "tried";
}else{$enter_check = "no";} 

if ($enter_check eq "yes"){
	my $fut_time=gmtime(time()+600)." GMT";  # Add 12 months (365 days)
	my $cookie_session = "session_user=$users{'session_id'}; path=/; expires=$fut_time;";
	my $cookie_user = "user_name=$pFORM{'user'}; path=/; expires=$fut_time;";
        print "Set-Cookie: " . $cookie_session . "\n";
        print "Set-Cookie: " . $cookie_user . "\n";
	$user_name = $pFORM{'user'};
	main();
}elsif ($session_user eq $users{'session_id'}) {
	my $fut_time=gmtime(time()+600)." GMT";  
	my $cookie = "session_user=$users{'session_id'}; path=/; expires=$fut_time;";
        print "Set-Cookie: " . $cookie . "\n";
	main();
}else{ 
	$login_error ="<strong>The username and/or password is incorrect.</strong>" if ($enter_check eq "tried");
 	login_screen(); }    


sub main(){
if ( !$FORM{'album'} && !$FORM{'image'}){
	show_galleries();
}
elsif ( $FORM{'album'} && $FORM{'image'} && $FORM{'display'} ==1 &&  $FORM{'type'})
{ 
	display_image($FORM{'album'},$FORM{'image'},$FORM{'type'});
}
elsif ( $FORM{'album'} && !$FORM{'image'}){
  show_album($FORM{'album'});
}
elsif ( $FORM{'album'} && $FORM{'image'})
{ 
  show_image($FORM{'album'},$FORM{'image'});
}
elsif ($FORM{'display'}==1 &&  $FORM{'type'}) 
{
	display_image("null","null",$FORM{'type'});
}
else {
print "nothing to see"; 	
}

}



sub show_galleries(){
print "Content-type: text/html\n\n";
print "<html><head><title>RememberWhen</title><meta name='viewport' content='width=device-width, initial-scale=.5' />";
print "
<style>
.loader {
        position: fixed;
        left: 0px;
        top: 0px;
        width: 100%;
        height:100%;
        z-index: 9999;
        background: url('$ENV{SCRIPT_NAME}?display=1&album=null&image=null&type=3') 50% 50% no-repeat rgb(194,194,194);
}
div.img {
    margin: 5px;
    padding: 5px;
    height: auto;
    width: auto;
    float: center;
    text-align: center;
}	

div.img img {
    display: inline;
    border-style: groove;
    margin: 5px;
    border: 5px solid #9B9999;
}

div.img a:hover img {
    border: 3px solid #0000ff;
}

div.desc {
  text-align: center;
  font-weight: normal;
}
h1.a {color: #363232; text-shadow: #363232 0.3em 0.3em 0.3em}
h1 span{
        color: #5379fa !important;
}
.myButton {
        display:inline-block;
        text-decoration:none;
        background: #cccccc;
        border: 1px solid #000000;
        cursor: pointer;
        border-radius: 2px;
        color: #000000;
        font-family: 'Exo', sans-serif;
        font-size: 16px;
        font-weight: 400;
        padding: 6px;
        margin-top: 10px;
}
.myButton:hover{
        opacity: 0.5;
        border: 1px solid #0000ff;
}

</style>";
print "</head><body bgcolor='#c2c2c2' text='#000000'>\n";
print "<div id='wait'  class='loader'></div>";
opendir my $dh, $rootDir
  or  print "oops, the resource you are looking for doesn't exist.";
  my @dirs = grep {-d "$rootDir/$_" && ! /^\.{1,2}$/} readdir($dh);
  closedir($dh);
  my @dirs = sorter($FORM{'oBy'});
  my $orderLink;
  if ($FORM{'oBy'} eq "name") {
	 $orderLink = "<a class='myButton' href=$ENV{SCRIPT_NAME}?oBy=date style='cursor:pointer;' title='Change order of albums'>Order by date added</a>";
  }elsif($FORM{'oBy'} eq "date") {
	 $orderLink = "<a class='myButton' href=$ENV{SCRIPT_NAME}?oBy=name style='cursor:pointer;' title='Change order of albums'>Order by name</a>";
  }else{
	 $orderLink = "<a class='myButton' href=$ENV{SCRIPT_NAME}?oBy=name style='cursor:pointer;' title='Change order of albums'>Order by name</a>";
  }
print "<center><h1 class='a'>Remember<span>When</span> $user_name</h1><hr></center>\n";
print "<a class='myButton' href=$ENV{SCRIPT_NAME}?logout=yes style='cursor:pointer;' title='Log out'>Logout</a>&nbsp;\n$orderLink<br><center>\n";
print  "<table border='0' cellspacing='2' cellpadding='2'>";
   my $row = 0;
foreach my $aaa (@dirs){
   my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($aaa->{mtime});
   #my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($aaa->{ctime});
   my $addedDate = ($mon + 1) ."/" .$mday . "/" . ($year + 1900);
   my $aa = $aaa->{path};
   $aa =~ s/(^.*\/)//g;
   my $nss =  $aa;
   $nss =~ s/ /\\ /g;
   my $dir = "$rootDir/$nss/Images";
   my @files = <$dir/*>;
   my $count = @files;
   my $random_number = int(rand($count)) + 1;   
   #$a =~ s/ /\ /g;
   print "<tr>\n" if ($row == 0);
   $row = ++$row;
        print "<td align='center' >\n";
	print "<div class='img'>";
        print "<a href='$ENV{SCRIPT_NAME}?album=$aa'>
	<img src='$ENV{SCRIPT_NAME}?display=1&album=$aa&image=$random_number&type=2'></a>";
        print "<div class='desc'>$aa<br><small>$addedDate</small></div>\n";
	print "</div>";
        print "</td>\n";
        if ($row == 4) {
           print "</tr>\n\n";
           $row = 0;
        }
}
print "</tr>" if $row != 4;
print "</table></center>";

print "<script>

 document.onreadystatechange = function () {
     if (document.readyState == 'complete') {
	var div = document.getElementById('wait');
	div.style.visibility='hidden'
   }
 }
</script>";

print "<br<br><hr><br><br></body></html>\n";
}


sub show_album{
   print "Content-type: text/html\n\n";
   print "<html><head><title>RememberWhen</title>
   <meta name='viewport' content='width=device-width, initial-scale=.5' />
<style>
div.img img {
    display: inline;
    margin: 5px;
    border: 3px solid #ffffff;
    border-radius: 10px;
     box-shadow:15px 15px 15px 5px grey;
}
div.img a:hover img {
        border: 3px solid #0000ff;
}
.loader {
        position: fixed;
        left: 0px;
        top: 0px;
        width: 100%;
        height: 100%;
        z-index: 9999;
        background: url('$ENV{SCRIPT_NAME}?display=1&album=null&image=null&type=3') 50% 50% no-repeat rgb(194,194,194);
}
h2.a {color: #363232; text-shadow: #363232 0.3em 0.3em 0.3em;line-height: 10px;}
.myButton {
        display:inline-block;
        text-decoration:none;
        background: #cccccc;
        border: 1px solid #000000;
        cursor: pointer;
        border-radius: 2px;
        color: #000000;
        font-family: 'Exo', sans-serif;
        font-size: 16px;
        font-weight: 400;
        padding: 6px;
        margin-top: 10px;
}
.myButton:hover{
        opacity: 0.5;
        border: 1px solid #0000ff;
}
h1.a {color: #363232; text-shadow: #363232 0.3em 0.3em 0.3em; line-height: 25px;}
h1 span{
        color: #5379fa !important;
} 

</style>
</head><body bgcolor='#c2c2c2' text='#000000'>\n";
print "<div id='wait'  class='loader'></div>";
print "<center><h1 class='a'>Remember<span>When</span> $user_name</h1></center>\n";
   print "<center><h2 class='a'>$FORM{album}</h2></center><hr>\n";
   print  "<a class='myButton' href=$ENV{SCRIPT_NAME}?logout=yes style='cursor:pointer;' title='Log out'>Logout</a>\n";
   print  "<a class='myButton' href=$ENV{SCRIPT_NAME} style='cursor:pointer;' title='show all albums'>Albums</a><center>\n";
   print  "<table cellspacing='2' cellpadding='2'>";
   my $row = 0;
    my $dir = "$rootDir/$FORM{'album'}/$thumbImages";
    opendir(DIR, $dir) or  print "oops, the resource you are looking for doesn't exist.";
    my @files = sort { $a <=> $b } readdir(DIR);
    while (my $file = shift @files) {
        # Use a regular expression to ignore files beginning with a period
        next if ($file =~ m/^\./);
	my $fileImage = $file;
	$fileImage =~ s{\.[^.]+$}{};
	print "<tr>\n" if ($row == 0);
	$row = ++$row;
	print "<td align='center' width='20%'>\n";
	print "<div class='img'><a href='$ENV{SCRIPT_NAME}?album=$FORM{album}&image=$fileImage'>";
	print "<img src='$ENV{SCRIPT_NAME}?display=1&album=$FORM{'album'}&image=$fileImage&type=2'></a></div>";
	print "</td>\n";
	if ($row == 5) { 
	   print "</tr>\n";
	   $row = 0;
	}
    }
    closedir(DIR);
print "</tr>" if $row != 5;
 print "</table></center>";
print "<script>

 document.onreadystatechange = function () {
     if (document.readyState == 'complete') {
        var div = document.getElementById('wait');
        div.style.visibility='hidden'
   }
 }
</script>";

print "<br<br><hr><br><br></body></html>\n";
}

sub show_image{
   my $nss =  $FORM{'album'};
   $nss =~ s/ /\\ /g;
   my $dir = "$rootDir/$nss/Images";
   my @files = <$dir/*>;
   my $count = @files;
   print "Content-type: text/html\n\n";
   print "<html><head><title>RememberWhen</title>
   <meta name='viewport' content='width=device-width, initial-scale=.5'>
	<style>
	.loader {
        position: fixed;
        left: 0px;
        top: 0px;
        width: 100%;
        height: 100%;
        z-index: 9999;
        background: url('$ENV{SCRIPT_NAME}?display=1&album=null&image=null&type=3') 50% 50% no-repeat rgb(194,194,194);
	}
	div.img img {
    	display: inline;
    	margin: 5px;
    	border: 5px solid #ffffff;
	border-radius: 10px;
	box-shadow:25px 25px 20px 5px black;
	}
.myButton {
        display:inline-block;
        text-decoration:none;
        background: #cccccc;
        border: 1px solid #000000;
        cursor: pointer;
        border-radius: 2px;
        color: #000000;
        font-family: 'Exo', sans-serif;
        font-size: 16px;
        font-weight: 400;
        padding: 6px;
        margin-top: 10px;
}
.myButton:hover{
        opacity: 0.5;
        border: 1px solid #0000ff;
}

h2.a {color: #363232; text-shadow: #363232 0.3em 0.3em 0.3em; line-height: 10px;}
h1.a {color: #363232; text-shadow: #363232 0.3em 0.3em 0.3em; line-height: 25px;}
h1 span{
        color: #5379fa !important;
}
</style>
   </head><body bgcolor='#c2c2c2' text='#000000'>\n";
   print "<div id='wait'  class='loader'></div>";
   print "<center><h1 class='a'>Remember<span>When</span> $user_name</h1></center>\n";
   print "<center><h2 class='a'>$FORM{album}</h2></center><hr>\n";
   print  "<a class='myButton' href=$ENV{SCRIPT_NAME}?logout=yes style='cursor:pointer;' title='Log out'>Logout</a>&nbsp;\n";
   print  "<a class='mybutton' href='$ENV{SCRIPT_NAME}' style='cursor:pointer;' title='show all albums'>Albums</a>&nbsp;";
   print  "<a class='mybutton' href='$ENV{SCRIPT_NAME}?album=$FORM{'album'}' style='cursor:pointer;' title='show current album'>Back to $FORM{album}</a>";
   my $prev = $FORM{'image'} -  1;
   $prev = 0 if ($prev < 1 );
   print  "<center><a class='mybutton' href='$ENV{SCRIPT_NAME}?album=$FORM{'album'}&image=$prev'> << </a>";
   print  "&nbsp&nbsp";
   my $next = $FORM{'image'} + 1;
   $next = 0 if ($next > $count);
   print  "<a class='mybutton' href='$ENV{SCRIPT_NAME}?album=$FORM{'album'}&image=$next'> >> </a>\n<br></center>";
   print "<center><div class='img'><img src='$ENV{SCRIPT_NAME}?display=1&album=$FORM{'album'}&image=$FORM{'image'}&type=1'></div></center> ";
   print "</center><br><br><br>";
print "<script>

 document.onreadystatechange = function () {
     if (document.readyState == 'complete') {
        var div = document.getElementById('wait');
        div.style.visibility='hidden'
   }
 }
</script>";

print "<br<br><hr><br><br></body></html>\n";
}

sub display_image{
	my ($album, $image, $type) = @_;
	my $getImage;
	if ($type == 1){
	        $getImage = "$rootDir/$album/$albumImages/$image.jpg";
		print "Content-type: image/jpeg\n\n";
	}elsif ($type == 2) {
		$getImage = "$rootDir/$album/$thumbImages/$image.jpg";
		print "Content-type: image/jpeg\n\n";
	}elsif ($type == 3){
                $getImage = "$supportImages/page-loader.gif";
                print "Content-type: image/gif\n\n";
	}else{
                $getImage = "$rootDir/$album/$thumbImages/$image.jpg";
                print "Content-type: image/jpeg\n\n";
	}
	my $buff;
	open IMAGE, "$getImage" or  open IMAGE, "$supportImages/noImage.jpg" ;
	while(read IMAGE, $buff, 1024) {
    		print $buff;
	}
	close IMAGE;
}


sub param_info(){
  my $rcvd_cookies = $ENV{'HTTP_COOKIE'};
  my @cookies = split /\;/, $rcvd_cookies;
  foreach my $cookie ( @cookies ){
     my($key, $val) = split(/=/, $cookie); # splits on the first =.
     $key =~ s/^\s+//;
     $val =~ s/^\s+//;
     $key =~ s/\s+$//;
     $val =~ s/\s+$//;
     if( $key eq "session_user" ){
        $session_user = $val;
     }
     if( $key eq "user_name" ){
        $user_name = $val;
     }
     
   }

        if (($ENV{'REQUEST_METHOD'} eq "GET") || ($ENV{'QUERY_STRING'})){
               my @form_data = split(/&/, $ENV{'QUERY_STRING'});
               foreach my $form (@form_data){
                        my @pairs  = split(/&/, $form);
                        foreach my $pair (@pairs) {
                        my ($key, $value) = split(/=/, $pair);
                        $value =~ tr/+/ /;
                        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
                        $FORM{$key} = $value;
                }
               }
        }
        if ($ENV{'REQUEST_METHOD'} eq "POST"){
                read(STDIN, my $buffer, $ENV{'CONTENT_LENGTH'});
                my @ppairs = split(/&/, $buffer);
                foreach my $ppair (@ppairs) {
                        my($pname, $pvalue) = split(/=/, $ppair);
                        $pvalue =~ tr/+/ /;
                        $pvalue =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
                        $pFORM{$pname} = $pvalue;
                }
        }
	if ($FORM{'oBy'} ne  ("name" || "date")) { $FORM{'oBy'} = "date"} ; 
}


sub sorter(){
    my $sortby = shift @_;
    my $dir =  $rootDir;
    #my $sortby ="date"; #3 date or name
    my $order = "des"; ## des is oldest first  or asc for newest first

    my @contents = read_dir($dir);
    my $sb       = $sortby eq 'date' ? 'mtime' : 'path';
    #my $sb       = $sortby eq 'date' ? 'ctime' : 'path';
    my @sorted   = sort { $a->{$sb} cmp $b->{$sb}  } @contents;
    @sorted      = reverse(@sorted) if ($order eq 'des') && ($sortby eq "date");
    return @sorted;
}

sub read_dir {
    # Takes a dir path.
    # Returns a list of file_info() hash refs.
    my $d = shift;
    opendir(my $dh, $d) or die $!;
    return map  { file_info($_) }  # Collect info.
           map  { "$d/$_" }        # Attach dir path.
           grep { ! /^\.{1,2}?$|^\.D.*/}
           #grep { ! /^\.\.?$/ }    # No dot dirs.
           readdir($dh);
}

sub file_info {
    # Takes a path to a file/dir.
    # Returns hash ref containing the path plus any stat() info you need.
    my $f = shift;
    my @s = stat($f);
    return {
        path  => $f,
	#ctime => $s[10],
        mtime => $s[9],
    };
}

sub login_screen{
print "Content-type: text/html\n\n";
print "
<html >
  <head>
    <title>Remember When</title>
    <meta name='viewport' content='width=device-width, initial-scale=.5' />
        <style>
body{
	margin: 0;
	padding: 0;
	background: ##c2c2c2;
	color: #000000;
	font-family: Arial;
	font-size: 12px;
}

.header{
	position: absolute;
	top: calc(29% - 55px);
	left: calc(40% - 48px);
	z-index: 2;
}

.header div{
	float: left;
	color: #000000;
	font-family: 'Exo', sans-serif;
	font-size: 35px;
	font-weight: 200;
}

.header div span{
	color: #5379fa !important;
}

.login{
	position: absolute;
	top: calc(40% - 75px);
	left: calc(40% - 50px);
	height: 150px;
	width: 350px;
	padding: 10px;
	z-index: 2;
}

.login input[type=text]{
	width: 250px;
	height: 30px;
	background: transparent;
	border: 1px solid rgba(0,0,0,0.6);
	border-radius: 2px;
	color: #000000;
	font-family: 'Exo', sans-serif;
	font-size: 18px;
	font-weight: 400;
	padding: 4px;
}

.login input[type=password]{
	width: 250px;
	height: 30px;
	background: transparent;
	border: 1px solid rgba(0,0,0,0.6);
	border-radius: 2px;
	color: #000000;
	font-family: 'Exo', sans-serif;
	font-size: 16px;
	font-weight: 400;
	padding: 4px;
	margin-top: 10px;
}

.login input[type=button]{
	width: 260px;
	height: 35px;
	background: #fff;
	border: 1px solid #000000;
	cursor: pointer;
	border-radius: 2px;
	color: #a18d6c;
	font-family: 'Exo', sans-serif;
	font-size: 16px;
	font-weight: 400;
	padding: 6px;
	margin-top: 10px;
}

.login input[type=submit]{
	width: 250px;
	height: 35px;
	background: #fff;
	border: 1px solid #000000;
	cursor: pointer;
	border-radius: 2px;
	color: #a18d6c;
	font-family: 'Exo', sans-serif;
	font-size: 16px;
	font-weight: 400;
	padding: 6px;
	margin-top: 10px;
}
.login input[type=submit]:hover{
	opacity: 0.5;
	color:#000000;
}
.login input[type=button]:hover{
	opacity: 0.8;
}

.login input[type=button]:active{
	opacity: 0.6;
}

.login input[type=text]:focus{
	outline: none;
	border: 2px solid rgba(255,255,255,0.9);
}

.login input[type=password]:focus{
	outline: none;
	border: 2px solid rgba(255,255,255,0.9);
}

.login input[type=submit]:focus{
	outline: none;
	border: 2px solid rgba(255,255,255,0.9);
}

::-webkit-input-placeholder{
   color: #567DF0;
}

::-moz-input-placeholder{
   color: #567DF0;
}
    </style>

<script>
function myFunction() {
   // document.getElementById('name').value = document.getElementById('field1').value;
   alert(document.getElementById('name').value);
}
</script>

    
  </head>

  <body bgcolor='#c2c2c2'>

    <div class='body'></div>
		<div class='grad'></div>
		<div class='header'>
			<div>Remember<span>When</span></div>
		</div>
		<div class='login'>
				$login_error";
	my $action;
	if ($FORM{'logout'}){
		 $action = $ENV{SCRIPT_NAME};
	}else { $action = $ENV{REQUEST_URI};}
	print "	<form action=$action method='post' >
		<input type='text' placeholder='username' name='user' id='name' autocapitalize='off'
                autocorrect='off'><br>
		<input type='password' placeholder='password' name='password'><br>
		<input type='submit'  value='Login'>
		<!-- input type='submit' onclick='myFunction()' value='Login' -->
		<!-- input type='button' onclick='myFunction()' value='Login' -->
		</form>
		</div>
  </body>
</html>";

}

