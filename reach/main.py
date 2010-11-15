#!/usr/bin/env python
# Reach, the remote acccess tool
# Copyright (C) 2010  Simon Poirier <simpoir@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from reach import opts, completor, sshconnector, term
from reach.settings import Settings
from reach.channel import Channel

def create_chain(completors, host_chain, visibility):
    """ Complete and lookup host recursively until it either:
        - gets a host without scope (public host)
        - gets a host in visibility
        - becomes ninja

    Returns a new (completed) chain.
    """
    if is_ninja():
        # ^ ninja is hidden. Find the ninja!
        return "NINJA!"

    # we assume sshConnector, for there are currently no other connectors
    conn = sshconnector.SshConnector()

    new_chain = list()

    # fill current chain, for we need connection info
    for chain_link in host_chain[1:]:
        new_link = dict(chain_link)
        reqs = conn.get_required(new_link)
        conn.get_defaults_completor().fill(host=new_link, requested=reqs)
        for compl in completors:
            compl.fill(host=new_link, requested=reqs)
        new_chain.insert(0, new_link)

    chain_tip = dict(host_chain[0])
    while True:
        new_chain.insert(0, chain_tip)
        reqs = conn.get_required(chain_tip)

        # do the completion
        conn.get_defaults_completor().fill(host=chain_tip, requested=reqs)
        for compl in completors:
            compl.fill(host=chain_tip, requested=reqs)

        # can we contact this host?
        if (not chain_tip.has_key('scope')) \
           or (chain_tip['scope'] in visibility):
            break

        # then do the chain lookup from completion info
        tip_choices = []
        for compl in completors:
            compl.lookup(host=chain_tip)

        if len(tip_choices) == 0:
            # We technically can't contact the start of the chain,
            # but I'm feeling lucky! let's try anyway.
            # If it works, visibility detection is broken (and it is)
            # or scope completion data is inaccurate (it probably is).
            print('Warning: incomplete connection chain. ' \
                  'Completion may be inaccurate.')
            break
        else:
            # save us a few lookups and just use the first choice.
            # Dijkstra was a fun/bad idea.
            chain_tip = dict(tip_choices[0])

    return new_chain


def discover_visibility():
    # TODO I have no idea how to do that yet.
    # Just return an empty tuple for the global scoped visibility.
    return tuple()


def main():
    completors = completor.init_completors(Settings.load())
    partial_host_chain = opts.get_initial_host_chain()
    current_visibility = discover_visibility()
    chain = create_chain(completors, partial_host_chain, current_visibility)

    chan = Channel.get_instance()
    chan.chain_connect(chain)
    chan.get_interactive_chan()

    term.set_raw()
    try:
        while chan.run():
            # run Forrest run
            pass
    finally:
        term.restore_tty()

if __name__ == "__main__":
    main()


