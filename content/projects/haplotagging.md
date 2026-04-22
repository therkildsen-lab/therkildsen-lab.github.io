+++
date = "2021-01-10 05:20:35"
draft = false
title = "Haplotagging"
description = "A low-cost linked-read technology for the masses"
[taxonomies]
tags = ["technology"]
[extra]
image = '/images/harpy.png'
+++

Next-generation sequencing has rapidly expanded genetics and genomics research. Short-read sequencing remains the most cost-effective and high-throughput option, while long-read technologies provide advantages like better genome assemblies, longer haplotypes, and improved detection of large structural variants.

Linked-read sequencing combines these strengths by using barcodes to tag DNA fragments from the same molecule. This keeps the low cost and high throughput of short reads while adding long-range information, making it easier to reconstruct haplotypes—something standard short-read data struggles to do.

This approach has been used in many areas, including genome assembly and population genomics, but some early commercial platforms were discontinued. Newer methods have since been developed, including haplotagging, which is cheaper, simpler, and does not require specialized equipment. Through an ongoing collaboration with the Cornell Genomics Innovation Hub,
we are expanding and improving on haplotagging linked-read chemistry.

However,wider adoption of these methods depends on accessible data analysis tools. Earlier technologies benefited from user-friendly software, but current linked-read approaches often rely on limited or platform-specific tools. To address this, we wrote Harpy, a user-friendly pipeline that processes haplotagging data from raw sequences through alignment, variant detection, and haplotype reconstruction, with workflows designed specifically for linked-read data.
