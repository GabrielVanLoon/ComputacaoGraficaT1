#!/usr/bin/env python3

# Obs: esse shader não considera que existem vértices de shader, usando a 
#      posição normalizada do atributo position para realizar os mapeamentos.

vertex_code = """
    attribute vec3 position;
    varying   vec2 fPosition;
    uniform   mat4 u_model_matrix;
    uniform   vec2 u_pattern_repeat;

    void main(){ 
        gl_Position = u_model_matrix * vec4(position, 1.0);

        // Prevent multiply by 0
        u_pattern_repeat.x = max(u_pattern_repeat.x, 1.0);
        u_pattern_repeat.y = max(u_pattern_repeat.y, 1.0);

        fPosition   = position.xy * u_pattern_repeat;
    }
"""

fragment_code = """
    varying vec2 fPosition;
    uniform vec2 u_pattern_repeat;
    uniform vec4 u_color;
    uniform float u_opacity;
    uniform sampler2D samplerTexture;

    void main(){ 
        vec2 textCoord = vec2((fPosition.x+1.0)/2.0, (fPosition.y+1.0)/2.0);
        vec4 texture = texture2D(samplerTexture, textCoord);
        gl_FragColor  = vec4(texture.xyz, u_opacity);
    }
"""