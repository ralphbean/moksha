<%namespace name="tw" module="tw2.core.mako_util"/>
<div ${tw.attrs(attrs=w.attrs)}>
  <script>
    moksha_feed_topic = '${w.topic[0]}';
  </script>
  <div id="LeftPane">
    ${w.feed_tree.display() | n}
  </div>
  <div id="RightPane">
    <div id="TopPane">
      ${w.feed_entries_tree.display() | n}
    </div>
    <div id="BottomPane"></div>
  </div>
</div>
