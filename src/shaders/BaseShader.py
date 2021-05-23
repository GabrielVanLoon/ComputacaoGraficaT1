#!/usr/bin/env python3

vertex_code = """
    attribute vec3 position;
    varying   vec3 fPosition;
    uniform   mat4 u_model_matrix;

    void main(){ 
        gl_Position = u_model_matrix * vec4(position, 1.0);
        fPosition   = gl_Position.xyz;
    }
"""

fragment_code = """
    varying vec3 fPosition;

    void main(){ 
        gl_FragColor  = vec4(1.0, 0.0, 0.0, 1.0);
    }
"""