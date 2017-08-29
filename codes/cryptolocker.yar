rule Cryptolocker
{
	meta:
        author = "Mert SARICA"
        description = "Cryptolocker Detection (February 2017 outbreak)"
		date = "2017/02/23"
		reference = "https://www.mertsarica.com"
		sample = "d01b54405d363850f8a45cfdf97693d2"
		sample = "291089237a4fb760d386dc89c701c09c"
		sample = "7fd6a6e66f5a99840947e752da8037f8"
		sample = "cf9f6eaf1cfb4c601fc868a8d893a72a"
		sample = "dd9849cbdec598a39cc7b82d1c4e28bc"		
		sample = "21bc751f05b78df9e0dd238595403c3c"		
		sample = "5b58e10f894602449424fc7de6a1e794"		
    version = "1.0"
    strings:
        $f1 = "String" nocase wide ascii       	
    condition:
        #f1 > 150 and filesize < 55KB
}