import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(1, 1, figsize=(22, 16))
ax.set_xlim(0, 22)
ax.set_ylim(0, 16)
ax.axis('off')
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('#F8F9FA')

# ── colours ──────────────────────────────────────────────────────────────────
COLOR_HEADER_MAIN   = '#2C3E50'   # main tables
COLOR_HEADER_SUPPORT= '#7F8C8D'   # supporting tables
COLOR_ROW_ODD       = '#FDFEFE'
COLOR_ROW_EVEN      = '#EBF5FB'
COLOR_ROW_PK        = '#FEF9E7'
COLOR_ROW_FK        = '#EAF2FF'
COLOR_BORDER        = '#2C3E50'
COLOR_BORDER_SUPPORT= '#95A5A6'
COLOR_TEXT          = '#2C3E50'
COLOR_TEXT_LIGHT    = '#ECF0F1'
COLOR_REL_LINE      = '#E74C3C'
COLOR_REL_LINE2     = '#8E44AD'

ROW_H   = 0.45   # row height
HDR_H   = 0.60   # header height

# ── helper: draw one table ────────────────────────────────────────────────────
def draw_table(ax, x, y, title, columns, header_color, border_color,
               width=3.8, tag_color=None):
    """columns: list of (name, type, tag) where tag in {'PK','FK','UQ','','NULL'}"""
    total_h = HDR_H + len(columns) * ROW_H
    # drop shadow
    shadow = FancyBboxPatch((x+0.07, y-total_h-0.07), width, total_h,
                            boxstyle='round,pad=0.05', linewidth=0,
                            facecolor='#BDC3C7', alpha=0.5, zorder=1)
    ax.add_patch(shadow)
    # header
    hdr = FancyBboxPatch((x, y-HDR_H), width, HDR_H,
                         boxstyle='round,pad=0.05', linewidth=1.5,
                         edgecolor=border_color, facecolor=header_color, zorder=2)
    ax.add_patch(hdr)
    ax.text(x + width/2, y - HDR_H/2, title,
            ha='center', va='center', fontsize=11, fontweight='bold',
            color=COLOR_TEXT_LIGHT, zorder=3)

    for i, (col_name, col_type, col_tag) in enumerate(columns):
        row_y = y - HDR_H - (i+1)*ROW_H
        bg = COLOR_ROW_PK if col_tag == 'PK' else \
             COLOR_ROW_FK if col_tag == 'FK' else \
             (COLOR_ROW_ODD if i % 2 == 0 else COLOR_ROW_EVEN)
        row = FancyBboxPatch((x, row_y), width, ROW_H,
                             boxstyle='square,pad=0', linewidth=0.8,
                             edgecolor='#BDC3C7', facecolor=bg, zorder=2)
        ax.add_patch(row)
        # column name
        ax.text(x + 0.18, row_y + ROW_H/2, col_name,
                ha='left', va='center', fontsize=8.5, color=COLOR_TEXT, zorder=3)
        # type
        ax.text(x + width - 1.2, row_y + ROW_H/2, col_type,
                ha='left', va='center', fontsize=7.5, color='#5D6D7E',
                style='italic', zorder=3)
        # tag badge
        if col_tag:
            badge_x = x + width - 0.38
            badge_color = '#F39C12' if col_tag == 'PK' else \
                          '#2980B9' if col_tag == 'FK' else \
                          '#27AE60' if col_tag == 'UQ' else '#95A5A6'
            badge = FancyBboxPatch((badge_x, row_y + 0.1), 0.32, 0.25,
                                   boxstyle='round,pad=0.03', linewidth=0,
                                   facecolor=badge_color, zorder=4)
            ax.add_patch(badge)
            ax.text(badge_x + 0.16, row_y + ROW_H/2, col_tag,
                    ha='center', va='center', fontsize=6, fontweight='bold',
                    color='white', zorder=5)

    # outer border
    outer = FancyBboxPatch((x, y-total_h), width, total_h,
                           boxstyle='round,pad=0.05', linewidth=1.8,
                           edgecolor=border_color, facecolor='none', zorder=5)
    ax.add_patch(outer)
    return total_h   # return table height for callers

# ── helper: draw relationship line ───────────────────────────────────────────
def draw_rel(ax, x1, y1, x2, y2, label, color=COLOR_REL_LINE):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=2, connectionstyle='arc3,rad=0.0'),
                zorder=6)
    mx, my = (x1+x2)/2, (y1+y2)/2
    ax.text(mx, my + 0.18, label, ha='center', va='bottom',
            fontsize=8, fontweight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                      edgecolor=color, linewidth=0.8), zorder=7)

# ═════════════════════════════════════════════════════════════════════════════
#  TABLE DEFINITIONS
# ═════════════════════════════════════════════════════════════════════════════

# ── USERS  (top-left) ─────────────────────────────────────────────────────────
users_cols = [
    ('id',                'bigint',   'PK'),
    ('name',              'varchar',  ''),
    ('email',             'varchar',  'UQ'),
    ('email_verified_at', 'timestamp','NULL'),
    ('password',          'varchar',  ''),
    ('remember_token',    'varchar',  'NULL'),
    ('created_at',        'timestamp',''),
    ('updated_at',        'timestamp',''),
]
draw_table(ax, 0.5, 15.2, 'users', users_cols,
           COLOR_HEADER_MAIN, COLOR_BORDER, width=4.2)

# ── EVENTS  (centre) ──────────────────────────────────────────────────────────
events_cols = [
    ('id',         'bigint',   'PK'),
    ('title',      'varchar',  ''),
    ('date',       'date',     ''),
    ('time',       'time',     ''),
    ('location',   'varchar',  ''),
    ('created_at', 'timestamp',''),
    ('updated_at', 'timestamp',''),
]
draw_table(ax, 8.5, 15.2, 'events', events_cols,
           COLOR_HEADER_MAIN, COLOR_BORDER, width=4.2)

# ── REGISTRATIONS  (bottom-centre) ───────────────────────────────────────────
reg_cols = [
    ('id',           'bigint',   'PK'),
    ('event_id',     'bigint',   'FK'),
    ('student_id',   'varchar',  ''),
    ('name',         'varchar',  ''),
    ('email',        'varchar',  ''),
    ('qr_token',     'varchar',  'UQ'),
    ('checked_in_at','timestamp','NULL'),
    ('created_at',   'timestamp',''),
    ('updated_at',   'timestamp',''),
]
draw_table(ax, 8.5, 10.2, 'registrations', reg_cols,
           COLOR_HEADER_MAIN, COLOR_BORDER, width=4.5)

# ── SESSIONS  (top-right) ─────────────────────────────────────────────────────
sess_cols = [
    ('id',            'varchar',  'PK'),
    ('user_id',       'bigint',   'FK'),
    ('ip_address',    'varchar',  'NULL'),
    ('user_agent',    'text',     'NULL'),
    ('payload',       'longtext', ''),
    ('last_activity', 'int',      ''),
]
draw_table(ax, 16.5, 15.2, 'sessions', sess_cols,
           COLOR_HEADER_SUPPORT, COLOR_BORDER_SUPPORT, width=4.2)

# ── PASSWORD_RESET_TOKENS  (left-bottom) ──────────────────────────────────────
prt_cols = [
    ('email',      'varchar',   'PK'),
    ('token',      'varchar',   ''),
    ('created_at', 'timestamp', 'NULL'),
]
draw_table(ax, 0.5, 10.2, 'password_reset_tokens', prt_cols,
           COLOR_HEADER_SUPPORT, COLOR_BORDER_SUPPORT, width=4.5)

# ── CACHE  (bottom-left) ──────────────────────────────────────────────────────
cache_cols = [
    ('key',        'varchar', 'PK'),
    ('value',      'medtext', ''),
    ('expiration', 'int',     ''),
]
draw_table(ax, 0.5, 6.2, 'cache', cache_cols,
           COLOR_HEADER_SUPPORT, COLOR_BORDER_SUPPORT, width=3.5)

# ── CACHE_LOCKS  (bottom-left 2) ─────────────────────────────────────────────
cl_cols = [
    ('key',        'varchar', 'PK'),
    ('owner',      'varchar', ''),
    ('expiration', 'int',     ''),
]
draw_table(ax, 4.5, 6.2, 'cache_locks', cl_cols,
           COLOR_HEADER_SUPPORT, COLOR_BORDER_SUPPORT, width=3.5)

# ── JOBS  (bottom-centre-right) ───────────────────────────────────────────────
jobs_cols = [
    ('id',           'bigint',  'PK'),
    ('queue',        'varchar', ''),
    ('payload',      'longtext',''),
    ('attempts',     'tinyint', ''),
    ('reserved_at',  'int',     'NULL'),
    ('available_at', 'int',     ''),
    ('created_at',   'int',     ''),
]
draw_table(ax, 8.5, 5.8, 'jobs', jobs_cols,
           COLOR_HEADER_SUPPORT, COLOR_BORDER_SUPPORT, width=4.0)

# ── FAILED_JOBS  (bottom-right) ───────────────────────────────────────────────
fj_cols = [
    ('id',         'bigint',    'PK'),
    ('uuid',       'varchar',   'UQ'),
    ('connection', 'text',      ''),
    ('queue',      'text',      ''),
    ('payload',    'longtext',  ''),
    ('exception',  'longtext',  ''),
    ('failed_at',  'timestamp', ''),
]
draw_table(ax, 13.2, 5.8, 'failed_jobs', fj_cols,
           COLOR_HEADER_SUPPORT, COLOR_BORDER_SUPPORT, width=4.2)

# ── JOB_BATCHES  (far-right-bottom) ──────────────────────────────────────────
jb_cols = [
    ('id',              'varchar', 'PK'),
    ('name',            'varchar', ''),
    ('total_jobs',      'int',     ''),
    ('pending_jobs',    'int',     ''),
    ('failed_jobs',     'int',     ''),
    ('failed_job_ids',  'longtext',''),
    ('options',         'medtext', 'NULL'),
    ('cancelled_at',    'int',     'NULL'),
    ('created_at',      'int',     ''),
    ('finished_at',     'int',     'NULL'),
]
draw_table(ax, 17.5, 10.2, 'job_batches', jb_cols,
           COLOR_HEADER_SUPPORT, COLOR_BORDER_SUPPORT, width=4.2)

# ═════════════════════════════════════════════════════════════════════════════
#  RELATIONSHIPS
# ═════════════════════════════════════════════════════════════════════════════

# events  →  registrations  (1 : N)
draw_rel(ax,
         x1=10.6, y1=11.35,   # bottom of events
         x2=10.6, y2=10.2,    # top of registrations
         label='1 : N', color='#E74C3C')

# users  →  sessions  (1 : N)
draw_rel(ax,
         x1=16.5, y1=13.5,    # left side of sessions
         x2=4.7,  y2=13.5,    # right side of users
         label='1 : N', color=COLOR_REL_LINE2)

# ═════════════════════════════════════════════════════════════════════════════
#  CARDINALITY NOTATION
# ═════════════════════════════════════════════════════════════════════════════

# crow's foot style labels
ax.text(10.6, 11.1,  '1', ha='center', va='top',    fontsize=10, fontweight='bold', color='#E74C3C')
ax.text(10.6, 10.35, 'N', ha='center', va='bottom', fontsize=10, fontweight='bold', color='#E74C3C')
ax.text(4.75, 13.65, '1', ha='right',  va='bottom', fontsize=10, fontweight='bold', color=COLOR_REL_LINE2)
ax.text(16.4, 13.65, 'N', ha='left',   va='bottom', fontsize=10, fontweight='bold', color=COLOR_REL_LINE2)

# ═════════════════════════════════════════════════════════════════════════════
#  LEGEND
# ═════════════════════════════════════════════════════════════════════════════

legend_x, legend_y = 0.5, 4.8
ax.text(legend_x, legend_y, 'Legend', fontsize=10, fontweight='bold', color=COLOR_TEXT)

badges = [
    ('#F39C12', 'PK', 'Primary Key'),
    ('#2980B9', 'FK', 'Foreign Key'),
    ('#27AE60', 'UQ', 'Unique'),
    ('#95A5A6', 'NULL', 'Nullable'),
]
for i, (bc, bt, bl) in enumerate(badges):
    bx = legend_x + i * 2.5
    by = legend_y - 0.45
    rect = FancyBboxPatch((bx, by), 0.42, 0.28,
                          boxstyle='round,pad=0.03', facecolor=bc,
                          linewidth=0, zorder=4)
    ax.add_patch(rect)
    ax.text(bx+0.21, by+0.14, bt, ha='center', va='center',
            fontsize=6.5, fontweight='bold', color='white', zorder=5)
    ax.text(bx+0.55, by+0.14, bl, ha='left', va='center',
            fontsize=8, color=COLOR_TEXT)

# rel-line legend
for i, (lc, lt) in enumerate([(COLOR_REL_LINE, 'events → registrations (CASCADE)'),
                               (COLOR_REL_LINE2, 'users → sessions')]):
    lx = legend_x + i * 5.5
    ly = legend_y - 1.0
    ax.plot([lx, lx+0.5], [ly, ly], color=lc, lw=2)
    ax.annotate('', xy=(lx+0.5, ly), xytext=(lx+0.3, ly),
                arrowprops=dict(arrowstyle='->', color=lc, lw=2))
    ax.text(lx+0.6, ly, lt, ha='left', va='center', fontsize=8, color=COLOR_TEXT)

# ═════════════════════════════════════════════════════════════════════════════
#  TITLE
# ═════════════════════════════════════════════════════════════════════════════
ax.text(11, 15.8, 'Event Registration & Attendance Information System',
        ha='center', va='center', fontsize=16, fontweight='bold',
        color=COLOR_HEADER_MAIN,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                  edgecolor=COLOR_BORDER, linewidth=1.5))
ax.text(11, 15.42, 'Entity-Relationship Diagram', ha='center', va='center',
        fontsize=11, color='#7F8C8D')

plt.tight_layout()
plt.savefig('/home/user/Event-Registration-and-Attendance-Information-System/er_diagram.png',
            dpi=180, bbox_inches='tight', facecolor='#F8F9FA')
print("ER diagram saved to er_diagram.png")
