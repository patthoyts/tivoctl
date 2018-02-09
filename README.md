# Python implementation of the TiVo® TCP Remote Protocol.

The [TiVo® TCP Remote Protocol](https://lv.tivo.com/assets/images/abouttivo/resources/downloads/brochures/TiVo_TCP_Network_Remote_Control_Protocol.pdf)
allows a TiVo Digital Video Recorder (DVR) to accept commands from the network equivalent to using the remote handset.

## Installation

## Command-line usage

This package may be used from the command-line to send commands from scripts.

    tivoctl --host <host> [command-type] [command-options]

e.g.:

    tivoctl --host tivo --ircode INFO DOWN DOWN SELECT
    tivoctl --host tivo --set-channel 101
    tivoctl --host tivo --keyboard STANDBY
    tivoctl --host tivo --teleport NOWPLAYING
    tivoctl --host tivo --get-channel


## Disclaimer

Tivo® is a trademark of TiVo Inc.

This software package is not affiliated with nor endorsed by TiVo Inc.