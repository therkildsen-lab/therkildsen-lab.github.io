+++
date = "2026-08-10 12:00:00"
title = "BLink-seq has landed"
description = "Linked-read sequencing for everyone"
[taxonomies]
tags = ["misc"]
[extra]
image = '/images/blinkseq.webp'
+++

What originally began as trying to adopt haplotagging linked-read sequencing from Frank Chan's laboratory group has grown into
into a significant collaboration with the Cornell Genomics Innovation Hub led by Jennifer Grenier and our own Azwad Iqbal. 
After years of trial and  error, Jennifer, Azwad, and the rest of the team developed BLink-seq, our take on approachable linked-read sequencing ([preprint](https://doi.org/10.64898/2026.08.03.742036)).

![BLink-seq in a nutshell](https://blinkseq.github.io/_astro/BLinkseq.B7NGO4jb_22k61m.webp)

BLink-seq stands for Bead-barcoded Linked-read sequencing (B+Link), and we developed it to share widely with the scientific
community. This is a pretty big deviation from other linked-read technologies which are:
- 10X Genomics: : proprietary commercial product discontinued 2019
- TELL-seq: proprietary commercial product
- stLFR: proprietary commercial product
- haplotagging: becoming a proprietary commercial product

Our commitment to this is serious: Pavel developed and maintins the [Harpy](https://github.com/pdimens/harpy) data processing
suite, along with other bioinformatics tools like the linked-read simulator ([Mimick](https://github.com/pdimens/mimick)) and 
a new version of the Lariat linked-read aligner ([Arachne](https://github.com/pdimens/mimick)). We also made sure the 
[BLink-seq website](https://blinkseq.github.io/) is more than just a showcase-- the full description and version-controlled
protocols are on there, and so is a wealth of information about linked-reads. So much so that we think it might be the only 
public-facing source of information and standards about linked-read data. The website covers general topics from general
explanations of linked-read data, to technical topics, data standards, and archival information.

This work has been and continues to be deeply collaborative. We have been inviting researchers from across the world to come 
and learn the technology from us and we now see BLink-seq being used across 4 continents! 