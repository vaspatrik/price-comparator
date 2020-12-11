from app import save_related_products

def upload():
	todo = [('Pet Toilet Tray', '11.9', 'Pet Dog Toilet Trainer Tray 3 Layers'), \
('Macbook 60w T shape', '21.40', 'macbook 60w, macbook 60w megsafe2, apple charger 60w T shape'), \
('Pet PlayPen 63*91*6 With Roof', '45.9', 'Dog Play Pen Rabbit Run Playpen Rabbit Pen'), \
('Pet Cage Blue 24 inches Single Door 700484', '29.04', '61 cm Foldable Pet Dog Crate Cage Kennel - Small'), \
('Foldable Soft Pet Carrier Crate', '47.7', 'Dog Crate for Indoor & Outdoor - Dog Home or Travel Crate'), \
('pet carrier backpack', '38.75', '49cm Pet Soft Cage '), \
('Pet Car Seat Cover', '19', 'Car Single Seat Front Cover for Dog Pet Seat Protector'), \
('10 Panel single door pet 80x80', '148', '10 Pannel Pet Play Pen'), \
('10 Panel single door pet 80x80', '159.08', 'Heavy Duty Temporary Fence 8 meters'), \
('8 Panel single door pet 80X80 700293', '108.45', 'Heavy Duty Temporary Fence 640cm '), \
('8 Panel single door pet 80X80 700293', '120.96', 'Indoor Outdoor Folding Metal Portable Puppy Exercise Pen (Dog )'), 
('8 panel double door pet', '112.49', '8 Pannel Double Doors Pet Cage'), \
('6 panel double door pet Pen', '89.63', '80 x 80 cm Double Door 6 Panels Pet Play Pen | Heavy Duty'), \
('Pet pan 8 panel single door 80x60 700762', '94.26', 'Dog Play Dog Pen '), \
('6 panel double door pet Pen', '79.52', 'Pet Play Pen Dog Pen | Heavy Duty'), \
('8 panel double door pet', '119.21', '8 Pannel Double Doors Pet Cage'), \
('10 Panel Single Door Pet Pen 80X100cm/80x80 double', '169.9', 'Dog Play Pen'), \
('10 Panel Single Door Pet Pen 80X100cm/80x80 double', '196', 'Temporary Fence 8 meters'), \
('Pet PlayPen 63*60*6 With Roof', '39.16', 'Rabbit PlayPen Dog Pet Play Pen 60 x 63CM - 6pcs With Shade Cover' ), \
('10 Panel Single Door Pet Pen 80X100cm/80x80 double', '197', 'Dog Play Pen'), \
('30 inches Double Doors Pet Cage 700592', '45.59', 'Dog Crate 76 cm Two Doors 30 inches Dog Crate - Medium '), \
('24 inches Single Door Pet Cage', '27.66', '61 cm Foldable Pet Dog Crate Cage Kennel - Small'), \
('48 inches Single Door Pet Cage', '94.05', '122 cm Dog Crate Dog Cage XXL 48 Inches Kennel'), \
('30 inches Single Door Pet Cage', '44.5', 'Medium Dog Cage 30 inches Dog Crate - Medium'), \
('36 inches Single Door Pet Cage', '60.8', 'Large 91 cm Dog Cage 36 inches Dog Crate - Large'), \
('36 inches Double Door Pet Cage', '63.64', 'Large 91 cm Two Doors Dog Cage 36 inches Dog Crate'), \
('42 inches Single Door Pet Cage', '80.51', 'Dog Crate 107 cm | XL Dog Cage 42 inches XL'), \
('Pet PlayPen 63*60*6 Without Roof', '33.9', 'Dog Pet Play Pen DOG Play Pen Collapsible Pet Puppy Kennel 24" 60 x 63CM - 6pcs'), \
('Pet Play Pen 63*60*8 With Roof', '44.28', 'Rabbit Run 8 Panels 24" With Cover  60cm x 63cm x 8pc '), \
('Pet Play Pen 63*60*8 Without Roof', '39.9', 'Rabbit Run 8 Panels 24" Dog Pet Play Pen 60 x 63CM - 8pcs'), \
('10 panel double door pet 80x80 700599', '147.9', 'Pet Play Pen 10 Panel Dog Play Pen'), \
('10 panel double door pet 80x80 700599', '157.64', 'Pet Play Pen 10 Panel Dog Play Pen'), \
('48 inches Double Door Pet Cage', '101.81', '48 inches Double Door Pet Cage 122 cm XXL'), \
('Electronic Pet Dog Fencing System', '40', 'Hidden Dog Pet Fencing System Electric Shock Collar Boundary Control'), \
('24 inches Double Doors Pet Cage 700591', '33.99', '24 inches Double Doors Pet Cage'), \
('Pet Partition 700620', '27.9', 'Dog Pet Car Cargo Barrier Universal'), \
('42 inches Double Door Pet Cage', '81.81', 'Dog Crate 107cm | XL Two Doors Dog Cage 42 inches XL')]
	for t in todo:
		save_related_products(t[0], [t[0]] + (t[2].split('|')), t[1])


