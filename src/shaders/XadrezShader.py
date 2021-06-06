#!/usr/bin/env python3

vertex_code = """
    attribute vec3 position;
    varying   vec3 fPosition;
    uniform   mat4 u_model_matrix;

    void main(){ 
        gl_Position = u_model_matrix * vec4(position, 1.0);
        fPosition   = position.xyz;
    }
"""

fragment_code = """
    varying vec3 fPosition;
    uniform vec4 u_color;

    void main(){ 
        // Declarando as cores do xadrez
        vec4 black = vec4(vec3(0.0), 1.0);
        vec4 white = vec4(vec3(1.0), 1.0);

        // Define a cor baseado na posicao (10x2)
        int yGrid = int((fPosition.y+1.0) * 10.0);
        int xGrid = int((fPosition.x+1.0) * 4.0);

        // Set shift in odd lines
        yGrid += (mod(xGrid, 2) == 1) ? 1 : 0;

        // gl_FragColor = (yGrid == 1 || yGrid == 3 || yGrid == 5) ? black : white;
        gl_FragColor = (mod(yGrid, 2) == 1) ? black : white;
    }
"""