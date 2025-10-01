import cadquery as cq

# Dimensiones en milímetros (cuerpo)
length = 70       # 7 cm
width = 42        # 4.2 cm
base_thickness = 1.7  # 1.7 mm
corner_radius = 11  # 11 mm
wall_height = 9   # 9 mm
wall_thickness = 1.7  # 1.7 mm

# Radio para el filete entre base y paredes
base_wall_fillet = 4.2  # Radio de redondeo para la unión base-pared

# Dimensiones del recorte de la pantalla
cutout_length = 17.6 # 17.6 mm
cutout_width = 25.5   # 25.5mm
cutout_offset_x = 12  # Desplazamiento en X

# Dimensiones de los agujeros para la pantalla
pillar_diameter = 1.8  # 1.8mm (diámetro del agujero interior)
pillar_wall_thickness = 1  # Grosor de la pared alrededor del agujero
pillar_outer_diameter = pillar_diameter + 2 * pillar_wall_thickness  # Diámetro exterior
pillar_height = 3     # 3mm (altura original)
pillar_wall_height = 1.5  # La mitad de la altura original
pillar_hole_depth = 2  # Profundidad del agujero
square_size = 22      # 2.2cm cuadrado imaginario para posicionar los pilares


# AÑADIR AGUJERO USB-C (reemplazando el agujero rectangular):
# Dimensiones del USB-C (coherentes con la trasera original)
usb_width = 9
usb_height = 3.8
usb_corner_radius = 1
usb_depth = 5  # Atraviesa ambas paredes
usb_vertical_offset = 3  # Altura del USB respecto a la base

# Dimensiones para paredes interiores adicionales
inner_wall_thickness = 0.8  # Grosor de las nuevas paredes interiores
inner_wall_height_extra = 2.2  # Las nuevas paredes serán 2.5mm más altas que las originales
inner_wall_start_height = 1  # Empezar un poco más arriba del filete

# Dimensiones del soporte USB-C
support_height = usb_vertical_offset  # Altura igual al offset del USB
support_length_x = 26.5  # 26.5mm en dirección X
support_length_y = 7   # 7mm en dirección Y

# Dimensiones del tope al final del soporte
tope_height = usb_vertical_offset + 3.6  # Altura del tope (más alto que el soporte)
tope_length_x = 2.4  # 2.4mm en dirección X
tope_length_y = support_length_y  # Mismas dimensiones en Y que el soporte

# ENFOQUE DE cajaRedondeada: Crear la forma exterior de la caja completa (base + paredes)
box_outer = (
    cq.Workplane("XY")
    .rect(length, width, centered=True)
    .extrude(wall_height + base_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# Crear la forma interior para vaciar la caja
box_inner = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)  # Comenzar desde la parte superior de la base
    .rect(length - 2*wall_thickness, width - 2*wall_thickness, centered=True)
    .extrude(wall_height)
    .edges("|Z")
    .fillet(corner_radius - wall_thickness)
)

# Crear la caja con el interior hueco
box = box_outer.cut(box_inner)

# Aplicar redondeo en la intersección interior entre base y paredes
box = box.edges("<<Z").fillet(base_wall_fillet)

# Crear el recorte en la base para la pantalla
screen_cutout = (
    cq.Workplane("XY")
    .center(cutout_offset_x, 0)  # Desplazar el centro de trabajo en X
    .rect(cutout_length, cutout_width)  # Crear el rectángulo de recorte
    .extrude(base_thickness + 0.1)  # Añadimos un poco más para asegurar que corta completamente
)

# Cortar el recorte de la pantalla de la caja
box = box.cut(screen_cutout)

# Crear las paredes interiores adicionales
inner_wall_outer = (
    cq.Workplane("XY")
    .workplane(offset=inner_wall_start_height)
    .rect(length - 2*wall_thickness, width - 2*wall_thickness, centered=True)
    .extrude(wall_height + base_thickness + inner_wall_height_extra - inner_wall_start_height)  # Ajustar altura
    .edges("|Z")
    .fillet(corner_radius - wall_thickness)
)

inner_wall_inner = (
    cq.Workplane("XY")
    .workplane(offset=inner_wall_start_height)  # Mismo nivel de inicio
    .rect(length - 2*wall_thickness - 2*inner_wall_thickness, 
          width - 2*wall_thickness - 2*inner_wall_thickness, centered=True)
    .extrude(wall_height + base_thickness + inner_wall_height_extra - inner_wall_start_height)
    .edges("|Z")
    .fillet(corner_radius - wall_thickness - inner_wall_thickness)
)

# Crear las paredes interiores
inner_walls = inner_wall_outer.cut(inner_wall_inner)

# Posiciones de los agujeros
half_square = square_size / 2
pillar_positions = [
    (half_square, half_square),   # Esquina superior derecha
    (half_square, -half_square),  # Esquina inferior derecha
    (-half_square, half_square),  # Esquina superior izquierda
    (-half_square, -half_square)  # Esquina inferior izquierda
]

# Crear las paredes circulares alrededor de los agujeros
pillar_walls = (
    cq.Workplane("XY")
    .center(cutout_offset_x, 0)  # Centrar en el mismo punto que el recorte
    .pushPoints(pillar_positions)
    .circle(pillar_outer_diameter / 2)  # Diámetro exterior
    .circle(pillar_diameter / 2)  # Diámetro interior (agujero)
    .extrude(base_thickness + pillar_wall_height)  # Extruir con la mitad de la altura original
)

# Crear los agujeros que NO atraviesan completamente la base (dejan 1mm en el fondo)
pillar_holes = (
    cq.Workplane("XY")
    .center(cutout_offset_x, 0)  # Centrar en el mismo punto que el recorte
    .pushPoints(pillar_positions)
    .circle(pillar_diameter / 2)  # Diámetro del agujero
    .extrude(-pillar_hole_depth)  # Profundidad del agujero (desde la parte superior)
)

# Dimensiones del hoyo circular del agujero del boton
button_hole_r = 4

button = (
    cq.Workplane("YZ")
    .workplane(offset=length / 2 - 3 )
    .center(0, base_thickness + wall_height)
    .circle(button_hole_r)
    .extrude(5)
)

button_support = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)  # Posicionar sobre la base interior
    .center(length/2 - wall_thickness - 5.2, 0)
    .rect(1.5, 9)  # Crear rectángulo del tope
    .extrude(wall_height - 1)  # Extruir hacia arriba (más alto que el soporte)
)

# Crear agujero USB-C en la pared frontal (la opuesta al recorte de pantalla)
usb_hole = (
    cq.Workplane("YZ")
    .workplane(offset=-length/2)  # Pared frontal (-X)
    .center(0, base_thickness + usb_vertical_offset + usb_height/2)  # Posición vertical ajustada
    .sketch()
    .rect(usb_width, usb_height)
    .vertices()
    .fillet(usb_corner_radius)
    .finalize()
    .extrude(usb_depth)  # Corta pared exterior + interior
)

# Crear el soporte rectangular para el USB-C
# Posicionado dentro de la carcasa, pegado a la pared interior donde está el agujero USB
usb_support = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)  # Posicionar sobre la base interior
    .center(-length/3 + 3.8, 0)  # Centrar pegado a la pared interior frontal
    .rect(support_length_x, support_length_y)  # Crear rectángulo de soporte
    .extrude(support_height)  # Extruir hacia arriba desde la base
)

# Crear el tope al final del soporte (más alto y más estrecho)
usb_tope = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)  # Posicionar sobre la base interior
    .center(-length/3 + 6.2 + support_length_x/2 - tope_length_x/2, 0)  # Posicionar al final del soporte
    .rect(tope_length_x, tope_length_y)  # Crear rectángulo del tope
    .extrude(tope_height)  # Extruir hacia arriba (más alto que el soporte)
)

# Crear el agujero en el medio del tope (desde la parte superior)
tope_hole = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness + tope_height)  # Posicionarse en la parte superior del tope
    .center(-length/3 + 6.2 + support_length_x/2 - tope_length_x/2, 0)  # Misma posición X,Y que el tope
    .circle(pillar_diameter/2)  # Usar el diámetro definido para los pilares
    .extrude(-tope_height/2)  # Hacer el agujero desde arriba hasta la mitad del tope
)

# Combinar todos los elementos y restar la hendidura, los agujeros y el agujero USB-C
result = (box
         .union(inner_walls)
         .union(pillar_walls)
         .union(usb_support)  # Agregar el soporte USB-C
         .union(usb_tope)     # Agregar el tope al final del soporte
         .union(button_support)
         .cut(pillar_holes)  # Hacer los agujeros en la base
         .cut(button)
         .cut(usb_hole)
         .cut(tope_hole))

# Mostrar el resultado
show_object(result)

# Exportar a STL
# cq.exporters.export(result, 'caraPantallaV31.stl')