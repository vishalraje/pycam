/*
 *      firewire_camera.h
 *      
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *      
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *      
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 *      MA 02110-1301, USA.
 */
#ifndef OPENEYESCAMERAREADER_H
#define OPENEYESCAMERAREADER_H

#include <cv.h>


// Exposed functions
int Get_Height();
int Get_Width();

void Grab_IEEE1394();
void Release_IEEE1394();
void Open_IEEE1394();
void Close_IEEE1394();
IplImage *Get_Raw_Frame(unsigned int cam_index);

#endif	// OPENEYESCAMERAREADER_H
