package fr.ensta.sysportapp.overview

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import fr.ensta.sysportapp.databinding.GridViewItemBinding
import fr.ensta.sysportapp.network.PersonInformation

/**
 * This class implements a [RecyclerView] [ListAdapter] which uses Data Binding to present [List]
 * data, including computing diffs between lists.
 */
class PhotoGridAdapter(val onClickListener: OnClickListener) : ListAdapter<PersonInformation, PhotoGridAdapter.PersonInformationViewHolder>(DiffCallback) {

    /**
     * The MarsPropertyViewHolder constructor takes the binding variable from the associated
     * GridViewItem, which nicely gives it access to the full [PersonInformation] information.
     */
    class PersonInformationViewHolder(private var binding: GridViewItemBinding):
        RecyclerView.ViewHolder(binding.root) {
        fun bind(personInformation: PersonInformation) {
            binding.information = personInformation
            // This is important, because it forces the data binding to execute immediately,
            // which allows the RecyclerView to make the correct view size measurements
            binding.executePendingBindings()
        }
    }

    /**
     * Allows the RecyclerView to determine which items have changed when the [List] of [PersonInformation]
     * has been updated.
     */
    companion object DiffCallback : DiffUtil.ItemCallback<PersonInformation>() {
        override fun areItemsTheSame(oldItem: PersonInformation, newItem: PersonInformation): Boolean {
            return oldItem === newItem
        }

        override fun areContentsTheSame(oldItem: PersonInformation, newItem: PersonInformation): Boolean {
            return oldItem.nom == newItem.nom && oldItem.prenom == newItem.prenom
        }
    }

    /**
     * Create new [RecyclerView] item views (invoked by the layout manager)
     */
    override fun onCreateViewHolder(parent: ViewGroup,
                                    viewType: Int): PersonInformationViewHolder {
        return PersonInformationViewHolder(GridViewItemBinding.inflate(LayoutInflater.from(parent.context)))
    }

    /**
     * Replaces the contents of a view (invoked by the layout manager)
     */
    override fun onBindViewHolder(holder: PersonInformationViewHolder, position: Int) {
        val personInformation = getItem(position)
        holder.itemView.setOnClickListener {
            onClickListener.onClick(personInformation)
        }
        holder.bind(personInformation)
    }

    class OnClickListener(val clickListener: (personInformation: PersonInformation) -> Unit) {
        fun onClick(personInformation:PersonInformation) = clickListener(personInformation)
    }
}
