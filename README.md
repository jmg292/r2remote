# What's this?

This is a wrapper around some radare2 functionality that's a part of a larger project I'm working on.  It should be fully portable and cross-platform. If it doesn't strike you as immediately useful, you would be correct! It has a very narrow and very specific use case.

# Implementation

A majority of the functionality for this program is implemented as a plug-in.  The rest of it simply exists to funnel data to and from those plugins over the network.

## Plugin system

The plugin system dynamically loads enabled scripts (declared in the configuration file) from the plugins folder into a single command handler.  Plugins MUST have a class that inherits from BaseCommandHandler in order to be picked up by the loader.  At load time, the command handler converts the class name as a string from CamelCase to snake_case.  This allows, for example, the handler method on the ListVolumes class to be called directly with the command list_volumes.

## Security

This application uses ECDSA keys over curve secp256k1 to provide transparent authentication.  A different set of ephemeral keys over the same curve is used to perfrom an ECDH handshake, which is then used to derive a symmetric encryption key for use during the session.  Once the key has been derived, messages are encrypted using chacha20/poly1305 and signed using the client's identity key.  This is all implemented in Rust and can be seen in the required repository https://github.com/jmg292/message_wrapper.

## Dependencies

I don't like dependencies, so most of this is just implemented using the standard library.  That being said, the program does depend on the [r2pipe](https://github.com/radareorg/radare2-r2pipe/tree/master/python) module, as well as the [message_wrapper](https://github.com/jmg292/message_wrapper) module referenced above.