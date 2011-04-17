<div id="${w.id}" class="containerPlus ${w.draggable} ${w.resizable}" style="top:${str(w.top)}px;left:${str(w.left)}px" buttons="${w.buttons}" skin="${w.skin}" icon="${w.icon}" width="${str(w.width)}" height="${str(w.height)}" dock="${w.dock}">
    <div class="no">
        <div class="ne">
            <div class="n">${w.title}</div>
        </div>
        <div class="o">
            <div class="e">
                <div class="c">
                    <div class="content">
                      ${w.content}
                    % if w.view_source:
                      <a href="#" onclick="$.ajax({
                              url: moksha.url('/widgets/code_widget?chrome=True&source=${w.widget_name}'),
                              success: function(r, s) {
                                  $('body').append(moksha.filter_resources(r));
                              }
                          });
                          return false;">View Source</a>
                      % endif
                    </div>
                </div>
            </div>
        </div>
        <div>
            <div class="so">
                <div class="se">
                    <div class="s"></div>
                </div>
            </div>
        </div>
    </div>
</div>
<script type="text/javascript">
jQuery('#${w.id}').buildContainers(
	${w._container_options}
);
</script>
