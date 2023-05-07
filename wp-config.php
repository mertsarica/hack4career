<?php
define( 'WP_CACHE', true );
/** 
 * The base configurations of the WordPress.
 *
 * This file has the following configurations: MySQL settings, Table Prefix,
 * Secret Keys, WordPress Language, and ABSPATH. You can find more information by
 * visiting {@link http://codex.wordpress.org/Editing_wp-config.php Editing
 * wp-config.php} Codex page. You can get the MySQL settings from your web host.
 *
 * This file is used by the wp-config.php creation script during the
 * installation. You don't have to use the web site, you can just copy this file
 * to "wp-config.php" and fill in the values.
 *
 * @package WordPress
 */
 //Added by WP-Cache Manager
// //Added by WP-Cache Manager
define( 'WPCACHEHOME', '/var/www/html/wp-content/plugins/wp-super-cache/' ); //Added by WP-Cache Manager
define( 'WP_AUTO_UPDATE_CORE', true );
// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'mertsarica_com');
/** MySQL database username */
define('DB_USER', 'hack4career');
/** MySQL database password */
define('DB_PASSWORD', '3GpkVDCDvOBUC25');
/** MySQL hostname */
define('DB_HOST', '50.116.59.22:65530');
/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');
define('WP_HOME','http://www.mertsarica.com');
define('WP_SITEURL','http://www.mertsarica.com');
// Enable Debug logging to the /wp-content/debug.log file
// define( 'WP_DEBUG', true );
// define( 'WP_DEBUG_DISPLAY', false );
// define( 'WP_DEBUG_LOG', true );
/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');
define('DISALLOW_FILE_EDIT', TRUE); // Sucuri Security: Fri, 21 Apr 2017 11:47:19 +0000
/**#@+
 * Authentication Unique Keys.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         '%?nZylh]eE)%) YIW+gf[pzjJv+:OI)d&d-:YWa4J*Y7JP^WrA]w>X+_o,Y@xW1,');
define('SECURE_AUTH_KEY',  'U i*v}R-R:etY_,Sd}hk)(|Ek.2?vAW7G[[SjswIP[@>H/t|-6_L)wc>?<m06B5X');
define('LOGGED_IN_KEY',    '30G45p+jNhLC%8f4/uo;!Ak|yAH!~~-j{pq-j]|+R.R?l|gQ7&;-#tA>d.LXX*hL');
define('NONCE_KEY',        '-|flL:<o>YB8R7m7xBVD}m:WC0g8?2u-7v5E1.KCl,?:G4 .CFhO$V][?d$VObgP');
define('AUTH_SALT',        'T*]|Bf$@5$I&O/:C+y)W,qh]-.3,=+Hz~-}20}l&`R2~tT`wKcxiHZROSY)we>P!');
define('SECURE_AUTH_SALT', '^V-MPZD^{>v0i3_82q[Y$U+wv9-W=Y$2Q?~q0O|azK}Z@y9<#2?/d*uWkep-85x;');
define('LOGGED_IN_SALT',   '%%U`S`wop|$9vye+U|y47k#G/izT,L2<J;j@Jdg@|2D+*ON1#VT)IX:J^gg9U^P8');
define('NONCE_SALT',       'S:kPc-5phC% _G1Ya-rs] sH3k;wp:56Ha>n#D}vs)X$l^A1a!aZn_&5bJetD*KL');
/**#@-*/
/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each a unique
 * prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'ms_';
/**
 * WordPress Localized Language, defaults to English.
 *
 * Change this to localize WordPress.  A corresponding MO file for the chosen
 * language must be installed to wp-content/languages. For example, install
 * de.mo to wp-content/languages and set WPLANG to 'de' to enable German
 * language support.
 */
define ('WPLANG', 'en_US');
/* That's all, stop editing! Happy blogging. */
/** WordPress absolute path to the Wordpress directory. */
if ( !defined('ABSPATH') )
  define('ABSPATH', dirname(__FILE__) . '/');
/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');
?>
