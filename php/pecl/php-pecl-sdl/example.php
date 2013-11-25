<?php
/**
 * Example of how to change screen properties such as title, icon or state using the PHP-SDL extension.
 *
 * @author Santiago Lizardo <santiagolizardo@php.net>
 */

// require 'common.php';

SDL_Init( SDL_INIT_VIDEO );

$screen = SDL_SetVideoMode( 640, 480, 16, SDL_HWSURFACE );
if( null == $screen )
{
	fprintf( STDERR, 'Error: %s' . PHP_EOL, SDL_GetError() );
}

for( $i = 3; $i > 0; $i-- )
{
	SDL_WM_SetCaption( "Switching to fullscreen mode in $i seconds...", null );
	SDL_Delay( 1000 );
}

SDL_WM_ToggleFullscreen( $screen );

SDL_Delay( 3000 );

SDL_WM_ToggleFullscreen( $screen );

SDL_WM_SetCaption( "Back from fullscreen mode. Quitting in 2 seconds...", null );

SDL_Delay( 2000 );

SDL_FreeSurface( $screen );

SDL_Quit();

