#!/usr/bin/env python3

vertex_code = """
    attribute vec3 position;
    varying   vec3 fPosition;
    uniform   mat4 u_model_matrix;
    uniform   mat4 u_time;

    void main(){ 
        gl_Position = u_model_matrix * vec4(position, 1.0);
        //fPosition = position.xyz;
        fPosition   = gl_Position.xyz;
    }
"""

fragment_code = """
// Noise animation - Lava (Adaptado por Gabriel Van Loon)
// by nimitz (twitter: @stormoid)
// https://www.shadertoy.com/view/lslXRS
// License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License
// Contact the author for other licensing options

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;

#define time iTime*0.1

    float hash21(in vec2 n){ 
        return fract(sin(dot(n, vec2(12.9898, 4.1414))) * 43758.5453); 
    }

    mat2 makem2(in float theta){
        float c = cos(theta);
        float s = sin(theta);
        return mat2(c,-s,s,c);
    }

    float random (in vec2 st) {
        return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
    }

    float noise( in vec2 st ){
        vec2 i = floor(st);
        vec2 f = fract(st);

        // Four corners in 2D of a tile
        float a = random(i);
        float b = random(i + vec2(1.0, 0.0));
        float c = random(i + vec2(0.0, 1.0));
        float d = random(i + vec2(1.0, 1.0));

        // Smooth Interpolation

        // Cubic Hermine Curve.  Same as SmoothStep()
        vec2 u = f*f*(3.0-2.0*f);
        // u = smoothstep(0.,1.,f);

        // Mix 4 coorners percentages
        return mix(a, b, u.x) +
                (c - a)* u.y * (1.0 - u.x) +
                (d - b) * u.x * u.y;
    }

    vec2 gradn(vec2 p){
        float ep = .09;
        float gradx = noise(vec2(p.x+ep,p.y))-noise(vec2(p.x-ep,p.y));
        float grady = noise(vec2(p.x,p.y+ep))-noise(vec2(p.x,p.y-ep));
        return vec2(gradx,grady);
    }

    float flow(in vec2 p){
        float z=2.;
        float rz = 0.;
        vec2 bp = p;
        for (float i= 1.;i < 7.;i++ )
        {
            //primary flow speed
            p += u_time*.6;
            
            //secondary flow speed (speed of the perceived flow)
            bp += u_time*1.9;
            
            //displacement field (try changing time multiplier)
            vec2 gr = gradn(i*p*.34+u_time*1.);
            
            //rotation of the displacement field
            gr*=makem2(u_time*6.-(0.05*p.x+0.03*p.y)*40.);
            
            //displace the system
            p += gr*.5;
            
            //add noise octave
            rz+= (sin(noise(p)*7.)*0.5+0.5)/z;
            
            //blend factor (blending displaced system with base system)
            //you could call this advection factor (.5 being low, .95 being high)
            p = mix(bp,p,.77);
            
            //intensity scaling
            z *= 1.4;
            //octave scaling
            p *= 2.;
            bp *= 1.9;
        }
        return rz;	
    }

    void main() {
        // Código Original
        vec2 p = gl_FragCoord.xy / u_resolution.xy-0.5;
        p.x *= u_resolution.x/u_resolution.y;

        p*= 3.;
        float rz = flow(p);

        // Original color
        //vec3 col = vec3(.2,0.07,0.01)/rz;
        vec3 col = vec3(0.495,0.150,0.117)/rz;
        col=pow(col,vec3(1.4));
        gl_FragColor = vec4(col,1.0);
    }
"""