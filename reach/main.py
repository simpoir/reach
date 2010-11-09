#!/usr/bin/env python

from reach import opts, completor
from reach.settings import Settings
from reach.channel import Channel

def create_chain(completors, host_chain, visibility):
    """ Complete and lookup host recursively until it either:
        - gets a host without scope (public host)
        - gets a host in visibility
        - becomes ninja
    """
    if is_ninja():
        # ^ ninja is hidden. Find the ninja!
        return "NINJA!"
    # TODO
    return []

def discover_visibility():
    # TODO I have no idea how to do that yet.
    return tuple()

def main():
    completors = completor.init_completors(Settings.load())
    partial_host_chain = opts.get_initial_host_chain()
    current_visibility = discover_visibility()
    chain = create_chain(completors, partial_host_chain, current_visibility)

    chan = Channel()
    chan.chain_connect(chain)
    while chan.run():
        # run Forrest run
        pass

if __name__ == "__main__":
    main()


